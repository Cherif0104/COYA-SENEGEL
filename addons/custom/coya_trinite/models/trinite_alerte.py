# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CoyaTriniteAlerte(models.Model):
    _name = "coya.trinite.alerte"
    _description = "Alerte Conseil Trinité"
    _order = "create_date desc"

    employee_id = fields.Many2one(
        "hr.employee",
        string="Employé",
        required=True,
        ondelete="cascade",
    )
    pilier = fields.Selection(
        [
            ("ndiguel", "Ndiguel (Productivité)"),
            ("barke", "Barké (Profitabilité)"),
            ("yar", "Yar (Professionnalisme)"),
        ],
        string="Pilier",
        required=True,
    )
    score = fields.Float("Score")
    seuil = fields.Float("Seuil", default=30.0)
    state = fields.Selection(
        [
            ("open", "Ouverte"),
            ("en_cours", "En cours"),
            ("surveillee", "Surveillée"),
            ("closed", "Fermée"),
            ("archivee", "Archivée"),
        ],
        string="État",
        default="open",
        required=True,
    )
