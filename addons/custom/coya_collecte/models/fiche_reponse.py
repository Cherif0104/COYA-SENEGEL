# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CoyaFicheReponse(models.Model):
    _name = "coya.fiche.reponse"
    _description = "Réponse à une fiche de collecte"
    _order = "date_received desc, id desc"

    fiche_type_id = fields.Many2one(
        "coya.fiche.type",
        string="Type de fiche",
        required=True,
        ondelete="cascade",
    )
    date_received = fields.Datetime("Date de réception", default=fields.Datetime.now, required=True)
    state = fields.Selection(
        [("draft", "Brouillon"), ("received", "Reçue")],
        string="État",
        default="received",
        required=True,
    )
    ligne_ids = fields.One2many(
        "coya.fiche.reponse.ligne",
        "reponse_id",
        string="Valeurs",
    )

    def get_value_by_champ(self, technical_name):
        """Retourne la valeur du champ par son nom technique."""
        for ligne in self.ligne_ids:
            if ligne.champ_id.technical_name == technical_name:
                return ligne.value_text
        return None


class CoyaFicheReponseLigne(models.Model):
    _name = "coya.fiche.reponse.ligne"
    _description = "Ligne de réponse (valeur par champ)"

    reponse_id = fields.Many2one(
        "coya.fiche.reponse",
        string="Réponse",
        required=True,
        ondelete="cascade",
    )
    champ_id = fields.Many2one(
        "coya.fiche.champ",
        string="Champ",
        required=True,
        ondelete="cascade",
    )
    value_text = fields.Text("Valeur")
