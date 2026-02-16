# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CoyaOpportunite(models.Model):
    _name = "coya.opportunite"
    _description = "Opportunité (pipeline prospection)"
    _order = "sequence desc, id desc"

    name = fields.Char("Objet", required=True)
    partner_id = fields.Many2one(
        "res.partner",
        string="Partenaire / Contact",
        ondelete="set null",
    )
    sequence = fields.Integer(default=10)
    stage = fields.Selection(
        [
            ("prospect", "Prospect"),
            ("qualification", "Qualification"),
            ("proposition", "Proposition"),
            ("negociation", "Négociation"),
            ("validation", "Validation"),
            ("gagne", "Gagné"),
            ("perdu", "Perdu"),
            ("en_attente", "En attente"),
            ("reporte", "Reporté"),
        ],
        string="Étape",
        default="qualification",
        required=True,
    )
    montant_estime = fields.Monetary(
        "Montant estimé",
        currency_field="currency_id",
    )
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id,
    )
    date_prevue = fields.Date("Date décision / clôture prévue")
    description = fields.Text("Description")
