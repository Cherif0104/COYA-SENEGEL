# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CoyaTechProjet(models.Model):
    _name = "coya.tech.projet"
    _description = "Projet technique (pipeline IT)"
    _order = "sequence, id desc"

    name = fields.Char("Nom du projet", required=True)
    description = fields.Text("Description")
    sequence = fields.Integer(default=10)
    etape = fields.Selection(
        [
            ("idee", "Idée"),
            ("poc", "POC"),
            ("dev", "Développement"),
            ("production", "Production"),
            ("maintenance", "Maintenance"),
        ],
        string="Étape",
        default="idee",
        required=True,
    )
    user_id = fields.Many2one(
        "res.users",
        string="Responsable",
        default=lambda self: self.env.user,
    )
