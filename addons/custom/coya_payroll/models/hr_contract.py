# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class HrContract(models.Model):
    _inherit = "hr.contract"

    wage_type = fields.Selection(
        [
            ("monthly", "Mensuel"),
            ("hourly", "Horaire"),
        ],
        string="Type de salaire",
        default="monthly",
    )
    hourly_rate = fields.Float(
        "Taux horaire",
        digits="Account",
        help="Utilisé si type horaire ou pour calcul des heures complémentaires.",
    )
