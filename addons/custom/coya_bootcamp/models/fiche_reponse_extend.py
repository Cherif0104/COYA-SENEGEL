# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CoyaFicheReponseExtend(models.Model):
    _inherit = "coya.fiche.reponse"

    bootcamp_id = fields.Many2one(
        "coya.bootcamp",
        string="Bootcamp",
        ondelete="set null",
    )
    cohorte_id = fields.Many2one(
        "coya.bootcamp.cohorte",
        string="Cohorte",
        ondelete="set null",
    )
