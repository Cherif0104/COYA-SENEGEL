# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CoyaStudioProjet(models.Model):
    _name = "coya.studio.projet"
    _description = "Projet de production (Studio)"
    _order = "sequence, id"

    name = fields.Char("Titre / Nom", required=True)
    description = fields.Text("Description")
    sequence = fields.Integer(default=10)
    etape = fields.Selection(
        [
            ("idee", "Idée"),
            ("preparation", "Préparation"),
            ("script", "Script"),
            ("validation_script", "Validation script"),
            ("preprod", "Préprod"),
            ("tournage", "Tournage"),
            ("montage", "Montage"),
            ("postprod", "Post-production"),
            ("validation", "Validation"),
            ("diffusion", "Diffusion"),
            ("archived", "Archivé"),
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
    date_debut = fields.Date("Début")
    date_fin_prevue = fields.Date("Fin prévue")
    budget_estime = fields.Monetary(
        "Budget estimé",
        currency_field="currency_id",
    )
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id,
    )
