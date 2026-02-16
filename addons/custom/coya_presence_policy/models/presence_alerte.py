# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CoyaPresenceAlerte(models.Model):
    _name = "coya.presence.alerte"
    _description = "Alerte présence (retard / absence non justifiée)"
    _order = "date desc, employee_id"

    employee_id = fields.Many2one(
        "hr.employee",
        string="Employé",
        required=True,
        ondelete="cascade",
        index=True,
    )
    date = fields.Date("Date", required=True, index=True)
    type_alerte = fields.Selection(
        [
            ("retard", "Retard"),
            ("absence_non_autorisee", "Absence non autorisée"),
        ],
        string="Type",
        required=True,
    )
    presence_day_id = fields.Many2one(
        "coya.presence.day",
        string="Jour concerné",
        ondelete="set null",
    )
    company_id = fields.Many2one(
        "res.company",
        related="employee_id.company_id",
        store=True,
    )
