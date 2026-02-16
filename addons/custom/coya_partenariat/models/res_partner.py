# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    partenaire_type = fields.Selection(
        [
            ("bailleur", "Bailleur"),
            ("partenaire_technique", "Partenaire technique"),
            ("institution", "Institution"),
            ("ong", "ONG"),
            ("entreprise", "Entreprise"),
            ("autre", "Autre"),
        ],
        string="Type partenaire",
    )
    partenaire_secteur = fields.Char("Secteur d'activité")
    partenaire_engagement = fields.Selection(
        [
            ("prospect", "Prospect"),
            ("contact_initial", "Contact initial"),
            ("en_cours", "Engagement en cours"),
            ("actif", "Partenaire actif"),
            ("en_veille", "En veille"),
            ("inactif", "Inactif"),
            ("resilie", "Résilié"),
        ],
        string="Niveau d'engagement",
    )
    partenaire_date_renouvellement = fields.Date(
        "Date renouvellement / prochaine échéance",
        help="Pour alertes sur les partenariats à renouveler.",
    )
