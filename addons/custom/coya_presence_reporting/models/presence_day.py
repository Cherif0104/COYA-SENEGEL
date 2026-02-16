# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CoyaPresenceDay(models.Model):
    _inherit = "coya.presence.day"

    department_id = fields.Many2one(
        "hr.department",
        related="employee_id.department_id",
        store=True,
        string="Département",
    )
