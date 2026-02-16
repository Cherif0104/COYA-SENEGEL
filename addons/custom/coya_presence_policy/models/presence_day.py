# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from datetime import datetime, time, timedelta

from odoo import api, fields, models


class CoyaPresenceDay(models.Model):
    _name = "coya.presence.day"
    _description = "Statut de présence par jour (employé)"
    _order = "date desc, employee_id"

    employee_id = fields.Many2one(
        "hr.employee",
        string="Employé",
        required=True,
        ondelete="cascade",
        index=True,
    )
    date = fields.Date("Date", required=True, index=True)
    status = fields.Selection(
        [
            ("present", "Présent"),
            ("absent", "Absent"),
            ("conge", "Congé"),
            ("maladie", "Maladie"),
            ("absence_autorisee", "Absence autorisée"),
            ("absence_non_autorisee", "Absence non autorisée"),
            ("retard", "Retard"),
            ("depart_anticipe", "Départ anticipé"),
            ("teletravail", "Télétravail"),
            ("formation", "Formation"),
            ("terrain", "Terrain"),
            ("deplacement", "Déplacement"),
            ("autre", "Autre"),
        ],
        string="Statut du jour",
        required=True,
    )
    hours_worked = fields.Float("Heures pointées", digits=(6, 2))
    leave_id = fields.Many2one(
        "hr.leave",
        string="Congé lié",
        ondelete="set null",
        help="Congé validé couvrant ce jour (si applicable).",
    )
    company_id = fields.Many2one(
        "res.company",
        related="employee_id.company_id",
        store=True,
    )

    _sql_constraints = [
        (
            "employee_date_uniq",
            "UNIQUE(employee_id, date)",
            "Une seule ligne par employé et par date.",
        )
    ]

    @api.model_create_multi
    def create(self, vals_list):
        recs = super().create(vals_list)
        recs._create_alerte_or_sanction_if_needed()
        return recs

    def write(self, vals):
        res = super().write(vals)
        if "status" in vals:
            self._create_alerte_or_sanction_if_needed()
        return res

    @api.model
    def _status_from_leave_type(self, leave):
        """Dérive le statut coya.presence.day à partir du type de congé."""
        if not leave or not leave.holiday_status_id:
            return "conge"
        name = (leave.holiday_status_id.name or "").lower()
        if "maladie" in name or "sick" in name:
            return "maladie"
        return "conge"

    @api.model
    def _compute_status_for_employee_date(self, employee, date):
        """
        Calcule le statut du jour pour un employé à une date donnée.
        Priorité : congé validé > pointage (activity_type) > absent.
        Retourne (status, hours_worked, leave_id).
        """
        hours_worked = 0.0
        leave_id = None
        status = "absent"

        # 1) Congé validé couvrant ce jour
        if hasattr(self.env["hr.leave"], "search"):
            day_start = datetime.combine(date, time.min)
            day_end = datetime.combine(date, time.max)
            domain = [
                ("employee_id", "=", employee.id),
                ("state", "=", "validate"),
                ("date_from", "<=", day_end),
                ("date_to", ">=", day_start),
            ]
            leaves = self.env["hr.leave"].search(domain, limit=1)
            if leaves:
                leave_id = leaves[0].id
                status = self._status_from_leave_type(leaves[0])
                return status, hours_worked, leave_id

        # 2) Pointage : coya.time.entry pour cet employé et ce jour
        entries = self.env["coya.time.entry"].search([
            ("employee_id", "=", employee.id),
            ("date", "=", date),
        ])
        if not entries:
            return "absent", 0.0, None

        hours_worked = sum(entries.mapped("unit_amount")) or 0.0
        # Statut dérivé des types d'activité : priorité aux statuts "négatifs"
        activity_priority = [
            "absence_non_autorisee",
            "retard",
            "depart_anticipe",
            "absence_autorisee",
            "maladie",
            "conge",
            "formation",
            "terrain",
            "deplacement",
            "teletravail",
        ]
        activity_type = entries[0].activity_type
        for at in activity_priority:
            if any(e.activity_type == at for e in entries):
                activity_type = at
                break
        status_map = {
            "conge": "conge",
            "maladie": "maladie",
            "absence_autorisee": "absence_autorisee",
            "absence_non_autorisee": "absence_non_autorisee",
            "retard": "retard",
            "depart_anticipe": "depart_anticipe",
            "formation": "formation",
            "terrain": "terrain",
            "deplacement": "deplacement",
            "teletravail": "teletravail",
        }
        status = status_map.get(activity_type, "present")
        return status, hours_worked, leave_id

    def _create_alerte_or_sanction_if_needed(self):
        """Pour les statuts retard / absence_non_autorisee, crée une alerte ou une sanction (3e = sanction)."""
        Alerte = self.env["coya.presence.alerte"]
        Sanction = self.env["coya.presence.sanction"]
        for day in self:
            if day.status not in ("retard", "absence_non_autorisee"):
                continue
            if not day.employee_id.company_id:
                continue
            # Éviter doublon : déjà une alerte ou sanction pour ce jour
            if Alerte.search_count([("presence_day_id", "=", day.id)]) or Sanction.search_count([("presence_day_id", "=", day.id)]):
                continue
            company = day.employee_id.company_id
            nb_avant = company.presence_nb_alertes_avant_sanction or 2
            type_incident = day.status
            count_alertes = Alerte.search_count([
                ("employee_id", "=", day.employee_id.id),
                ("type_alerte", "=", type_incident),
            ])
            if count_alertes < nb_avant:
                Alerte.create({
                    "employee_id": day.employee_id.id,
                    "date": day.date,
                    "type_alerte": type_incident,
                    "presence_day_id": day.id,
                })
            else:
                montant = self.env["coya.presence.sanction"]._compute_sanction_amount(day.employee_id)
                Sanction.create({
                    "employee_id": day.employee_id.id,
                    "date": day.date,
                    "type_sanction": type_incident,
                    "presence_day_id": day.id,
                    "montant": montant,
                })

    @api.model
    def update_range(self, date_from, date_to, employee_ids=None):
        """Met à jour les statuts pour une plage de dates et optionnellement une liste d'employés."""
        if employee_ids is None:
            employee_ids = self.env["hr.employee"].search([("company_id", "!=", False)]).ids
        employees = self.env["hr.employee"].browse(employee_ids)
        d = date_from
        while d <= date_to:
            for emp in employees:
                self.update_for_employee_date(emp, d)
            d += timedelta(days=1)
        return True
