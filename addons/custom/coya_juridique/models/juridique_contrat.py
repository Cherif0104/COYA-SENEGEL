# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CoyaJuridiqueContrat(models.Model):
    _name = "coya.juridique.contrat"
    _description = "Contrat (suivi juridique)"
    _order = "date_fin_effet desc"

    name = fields.Char("Objet / Référence", required=True)
    partner_id = fields.Many2one(
        "res.partner",
        string="Partenaire",
        ondelete="restrict",
    )
    date_debut = fields.Date("Début d'effet")
    date_fin_effet = fields.Date("Fin d'effet", help="Date d'échéance pour renouvellement")
    type_contrat = fields.Selection(
        [
            ("partenariat", "Partenariat"),
            ("subvention", "Subvention"),
            ("prestation", "Prestation"),
            ("emploi", "Emploi"),
            ("autre", "Autre"),
        ],
        string="Type",
        default="autre",
    )
    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("actif", "Actif"),
            ("a_renouveler", "À renouveler"),
            ("en_renouvellement", "En renouvellement"),
            ("expire", "Expiré"),
            ("resilie", "Résilié"),
            ("suspendu", "Suspendu"),
        ],
        string="État",
        default="actif",
    )
    notes = fields.Text("Notes")
