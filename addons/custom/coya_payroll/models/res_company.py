# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    cnss_employee_rate = fields.Float(
        "Taux CNSS salarial (%)",
        digits=(5, 2),
        help="Part salariale CNSS (Sénégal).",
    )
    cnss_employer_rate = fields.Float(
        "Taux CNSS patronal (%)",
        digits=(5, 2),
    )
    amo_rate = fields.Float(
        "Taux AMO (%)",
        digits=(5, 2),
    )
    mutuelle_employee = fields.Float(
        "Mutuelle part salariale",
        digits="Account",
    )
