# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import models


class HrLeave(models.Model):
    _inherit = "hr.leave"

    def write(self, vals):
        res = super().write(vals)
        if vals.get("state") == "validate":
            self._update_presence_days_for_leave()
        return res

    def _update_presence_days_for_leave(self):
        """Met à jour coya.presence.day pour chaque jour couvert par le congé validé."""
        PresenceDay = self.env["coya.presence.day"]
        for leave in self:
            if leave.state != "validate" or not leave.employee_id:
                continue
            date_from = leave.date_from.date() if hasattr(leave.date_from, "date") else leave.date_from
            date_to = leave.date_to.date() if hasattr(leave.date_to, "date") else leave.date_to
            d = date_from
            while d <= date_to:
                PresenceDay.update_for_employee_date(leave.employee_id, d)
                d += timedelta(days=1)
