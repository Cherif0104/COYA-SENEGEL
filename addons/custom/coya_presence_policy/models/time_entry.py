# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import api, models
from odoo.exceptions import ValidationError


class CoyaTimeEntry(models.Model):
    _inherit = "coya.time.entry"

    def _presence_day_update_employee_dates(self):
        """Met à jour coya.presence.day pour les (employee_id, date) concernés."""
        PresenceDay = self.env["coya.presence.day"]
        for entry in self:
            if entry.employee_id and entry.date:
                PresenceDay.update_for_employee_date(entry.employee_id, entry.date)

    @api.model_create_multi
    def create(self, vals_list):
        recs = super().create(vals_list)
        recs._presence_day_update_employee_dates()
        return recs

    def write(self, vals):
        res = super().write(vals)
        if any(k in vals for k in ("employee_id", "date", "unit_amount", "activity_type")):
            self._presence_day_update_employee_dates()
        return res

    def unlink(self):
        employees_dates = [(e.employee_id, e.date) for e in self if e.employee_id and e.date]
        res = super().unlink()
        PresenceDay = self.env["coya.presence.day"]
        for emp, date in employees_dates:
            if emp.exists():
                PresenceDay.update_for_employee_date(emp, date)
        return res

    @api.constrains("employee_id", "date", "unit_amount")
    def _check_plafond_heures_jour(self):
        for entry in self:
            if not entry.employee_id or not entry.date:
                continue
            emp = entry.employee_id
            if not emp.presence_policy_apply:
                continue
            plafond = emp.presence_plafond_heures_jour or emp.company_id.presence_plafond_heures_jour or 10.0
            same_day = self.search([
                ("employee_id", "=", emp.id),
                ("date", "=", entry.date),
                ("id", "!=", entry.id),
            ])
            total = sum(same_day.mapped("unit_amount")) + (entry.unit_amount or 0)
            if total > plafond:
                raise ValidationError(
                    "Le cumul des heures pour %s le %s (%.2f h) dépasse le plafond autorisé (%.1f h/jour)."
                    % (emp.name, entry.date, total, plafond)
                )
