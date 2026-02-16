# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CoyaJuridiqueContentieux(models.Model):
    _name = "coya.juridique.contentieux"
    _description = "Contentieux"
    _order = "date_ouverture desc"

    name = fields.Char("Objet", required=True)
    reference = fields.Char("Référence / N° dossier")
    date_ouverture = fields.Date("Date d'ouverture", default=fields.Date.context_today)
    part_autre = fields.Many2one(
        "res.partner",
        string="Partie adverse",
        ondelete="set null",
    )
    type_contentieux = fields.Selection(
        [
            ("civil", "Civil"),
            ("commercial", "Commercial"),
            ("travail", "Travail"),
            ("administratif", "Administratif"),
            ("autre", "Autre"),
        ],
        string="Type",
        default="autre",
    )
    state = fields.Selection(
        [
            ("ouvert", "Ouvert"),
            ("en_cours", "En cours"),
            ("cloture", "Clôturé"),
        ],
        string="État",
        default="ouvert",
    )
    description = fields.Text("Description")
