# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CoyaBootcampIntervenant(models.Model):
    _name = "coya.bootcamp.intervenant"
    _description = "Intervenant (formateur, coach, mentor)"
    _order = "cohorte_id, sequence"

    cohorte_id = fields.Many2one(
        "coya.bootcamp.cohorte",
        string="Cohorte",
        required=True,
        ondelete="cascade",
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Personne",
        required=True,
        ondelete="cascade",
    )
    role = fields.Selection(
        [
            ("formateur", "Formateur"),
            ("coach", "Coach"),
            ("mentor", "Mentor"),
            ("autre", "Autre"),
        ],
        string="Rôle",
        required=True,
        default="formateur",
    )
    sequence = fields.Integer("Ordre", default=10)
