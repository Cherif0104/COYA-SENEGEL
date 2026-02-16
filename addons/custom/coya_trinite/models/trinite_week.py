# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models


class CoyaTriniteWeek(models.Model):
    _name = "coya.trinite.week"
    _description = "Période hebdomadaire Trinité (cycle Xalima)"
    _order = "week_start desc"

    week_start = fields.Date("Lundi", required=True, index=True)
    week_end = fields.Date("Vendredi", compute="_compute_week_end", store=True)
    state = fields.Selection(
        [("open", "Ouverte"), ("closed", "Clôturée")],
        default="open",
        required=True,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Société",
        default=lambda self: self.env.company,
    )

    _sql_constraints = [
        ("week_uniq", "UNIQUE(week_start, company_id)", "Une seule période par semaine et société."),
    ]

    @api.depends("week_start")
    def _compute_week_end(self):
        for rec in self:
            if rec.week_start:
                rec.week_end = rec.week_start + timedelta(days=4)  # vendredi
            else:
                rec.week_end = False

    @api.model
    def _get_week_bounds(self, date=None):
        """Retourne (lundi, vendredi) de la semaine de date (ou semaine courante)."""
        date = date or fields.Date.context_today(self)
        week_start = date - timedelta(days=date.weekday())
        week_end = week_start + timedelta(days=4)
        return week_start, week_end

    def action_close_week(self):
        """Clôture la période : crée les scores manquants (0) et crée les alertes."""
        Score = self.env["coya.trinite.score"]
        for week in self:
            if week.state == "closed":
                continue
            employees = self.env["hr.employee"].search([("company_id", "=", week.company_id.id)])
            for emp in employees:
                existing = Score.search([
                    ("employee_id", "=", emp.id),
                    ("periode_start", "=", week.week_start),
                    ("periode_end", "=", week.week_end),
                ], limit=1)
                if not existing:
                    Score.create({
                        "employee_id": emp.id,
                        "periode_start": week.week_start,
                        "periode_end": week.week_end,
                        "score_ndiguel": 0.0,
                        "score_barke": 0.0,
                        "score_yar": 0.0,
                    })
            week.state = "closed"
        return True

    @api.model
    def cron_friday_close(self):
        """Appelé par le cron vendredi soir : clôture la semaine courante."""
        week_start, week_end = self._get_week_bounds()
        week = self.search([
            ("week_start", "=", week_start),
            ("company_id", "in", self.env.companies.ids),
        ], limit=1)
        if not week:
            week = self.create({"week_start": week_start, "state": "open"})
        if week.state == "open":
            week.action_close_week()

    @api.model
    def cron_daily_reminder(self):
        """Rappel quotidien : notification ou mail pour remplir les champs Trinité / Xalima."""
        # Envoyer une notification aux utilisateurs (ex. groupe Qualité ou tous)
        # Pour l'instant on ne fait rien de plus (pas de mail template dans le plan minimal)
        return True

    @api.model
    def action_point_vendredi(self):
        """Ouvre la synthèse de la semaine courante (scores) et la période hebdo pour clôture."""
        week_start, week_end = self._get_week_bounds()
        week = self.search([
            ("week_start", "=", week_start),
            ("company_id", "in", self.env.companies.ids),
        ], limit=1)
        if not week:
            week = self.create({"week_start": week_start, "state": "open"})
        return {
            "type": "ir.actions.act_window",
            "name": "Point vendredi – Semaine du %s" % week_start,
            "res_model": "coya.trinite.score",
            "view_mode": "list,form",
            "domain": [
                ("periode_start", "=", week_start),
                ("periode_end", "=", week_end),
            ],
            "context": {
                "default_periode_start": week_start,
                "default_periode_end": week_end,
                "default_employee_id": False,
            },
        }
