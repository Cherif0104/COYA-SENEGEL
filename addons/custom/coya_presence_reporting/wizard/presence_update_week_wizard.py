# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models


class PresenceUpdateWeekWizard(models.TransientModel):
    _name = "coya.presence.update.week.wizard"
    _description = "Mettre à jour les synthèses hebdo"

    week_start = fields.Date("Lundi de la semaine", required=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if "week_start" in res or "week_start" in (fields_list or []):
            today = fields.Date.context_today(self)
            # lundi
            delta = today.weekday()
            res.setdefault("week_start", today - timedelta(days=delta))
        return res

    def action_update_weeks(self):
        self.ensure_one()
        Week = self.env["coya.presence.week"]
        employees = self.env["hr.employee"].search([("company_id", "!=", False)])
        for emp in employees:
            Week.update_week(emp, self.week_start)
        return {
            "type": "ir.actions.act_window",
            "name": "Synthèse semaine du %s" % self.week_start,
            "res_model": "coya.presence.week",
            "view_mode": "list",
            "domain": [("week_start", "=", self.week_start)],
        }
