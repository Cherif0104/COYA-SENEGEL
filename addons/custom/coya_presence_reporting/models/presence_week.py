# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CoyaPresenceWeek(models.Model):
    _name = "coya.presence.week"
    _description = "Synthèse présence par semaine (employé)"
    _order = "week_start desc, employee_id"

    employee_id = fields.Many2one(
        "hr.employee",
        string="Employé",
        required=True,
        ondelete="cascade",
        index=True,
    )
    week_start = fields.Date("Lundi semaine", required=True, index=True)
    hours_total = fields.Float("Heures pointées", digits=(6, 2))
    hours_target = fields.Float("Heures cibles", digits=(6, 2), help="Ex. 44 h/semaine")
    hours_gap = fields.Float("Écart (h)", digits=(6, 2), help="heures_total - hours_target")
    company_id = fields.Many2one(
        "res.company",
        related="employee_id.company_id",
        store=True,
    )
    department_id = fields.Many2one(
        "hr.department",
        related="employee_id.department_id",
        store=True,
    )

    _sql_constraints = [
        (
            "employee_week_uniq",
            "UNIQUE(employee_id, week_start)",
            "Une seule ligne par employé et par semaine.",
        )
    ]

    @api.model
    def _week_start(self, date):
        """Retourne le lundi de la semaine de date."""
        if not date:
            return None
        # weekday(): Monday = 0, Sunday = 6
        from datetime import timedelta
        delta = date.weekday()
        return date - timedelta(days=delta)

    @api.model
    def update_week(self, employee, week_start):
        """Crée ou met à jour la synthèse hebdo pour (employé, semaine)."""
        from datetime import timedelta
        week_end = week_start + timedelta(days=6)
        days = self.env["coya.presence.day"].search([
            ("employee_id", "=", employee.id),
            ("date", ">=", week_start),
            ("date", "<=", week_end),
        ])
        hours_total = sum(days.mapped("hours_worked")) or 0.0
        target = employee.presence_heures_cibles_semaine or employee.company_id.presence_heures_cibles_semaine or 44.0
        if not employee.presence_policy_apply:
            target = 0.0
        hours_gap = hours_total - target
        rec = self.search([
            ("employee_id", "=", employee.id),
            ("week_start", "=", week_start),
        ], limit=1)
        vals = {
            "employee_id": employee.id,
            "week_start": week_start,
            "hours_total": hours_total,
            "hours_target": target,
            "hours_gap": hours_gap,
        }
        if rec:
            rec.write(vals)
        else:
            rec = self.create(vals)
        return rec
