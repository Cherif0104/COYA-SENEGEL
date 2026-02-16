# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CoyaJuridiqueRisque(models.Model):
    _name = "coya.juridique.risque"
    _description = "Risque juridique"
    _order = "gravite desc, date_identification desc"

    name = fields.Char("Libellé", required=True)
    type_risque = fields.Selection(
        [
            ("contractuel", "Contractuel"),
            ("conformite", "Conformité"),
            ("contentieux", "Contentieux"),
            ("autre", "Autre"),
        ],
        string="Type",
        default="autre",
    )
    gravite = fields.Selection(
        [
            ("faible", "Faible"),
            ("moyen", "Moyen"),
            ("eleve", "Élevé"),
            ("critique", "Critique"),
        ],
        string="Gravité",
        default="moyen",
    )
    date_identification = fields.Date("Date d'identification", default=fields.Date.context_today)
    description = fields.Text("Description")
    mesure_prevue = fields.Text("Mesure prévue / Mitigation")
    state = fields.Selection(
        [
            ("ouvert", "Ouvert"),
            ("en_cours", "En cours de traitement"),
            ("cloture", "Clôturé"),
        ],
        string="État",
        default="ouvert",
    )
