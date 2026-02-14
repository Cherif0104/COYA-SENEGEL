# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CoyaBootcamp(models.Model):
    _name = "coya.bootcamp"
    _description = "Bootcamp"

    name = fields.Char("Nom", required=True)
    description = fields.Text("Description")
    partner_id = fields.Many2one(
        "res.partner",
        string="Partenaire / Financeur",
        help="Ex. UEMOA, Chambre des métiers, JMOA",
    )
    cohorte_ids = fields.One2many(
        "coya.bootcamp.cohorte",
        "bootcamp_id",
        string="Cohortes / Sessions",
    )
