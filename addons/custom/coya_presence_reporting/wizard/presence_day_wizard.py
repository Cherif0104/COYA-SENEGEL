# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PresenceDayWizard(models.TransientModel):
    _name = "coya.presence.day.wizard"
    _description = "Vue présences par jour"

    date = fields.Date("Date", required=True, default=fields.Date.context_today)

    def action_open_day_view(self):
        """Ouvre la liste des présences filtrée sur la date choisie."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Présences au %s" % self.date,
            "res_model": "coya.presence.day",
            "view_mode": "list,pivot",
            "domain": [("date", "=", self.date)],
            "context": {"search_default_date": self.date},
        }
