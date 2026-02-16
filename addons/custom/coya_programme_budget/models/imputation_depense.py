# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CoyaImputationDepense(models.Model):
    _name = "coya.imputation.depense"
    _description = "Imputation de dépense sur une ligne budgétaire"
    _order = "date desc, id desc"

    ligne_budgetaire_id = fields.Many2one(
        "coya.ligne.budgetaire",
        string="Ligne budgétaire",
        required=True,
        ondelete="cascade",
    )
    projet_id = fields.Many2one(
        "coya.projet",
        related="ligne_budgetaire_id.projet_id",
        store=True,
    )
    programme_id = fields.Many2one(
        "coya.programme",
        related="ligne_budgetaire_id.programme_id",
        store=True,
    )
    montant = fields.Monetary(
        "Montant",
        required=True,
        currency_field="currency_id",
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="ligne_budgetaire_id.currency_id",
        store=True,
    )
    date = fields.Date("Date", default=fields.Date.context_today)
    reference = fields.Char(
        "Référence / Pièce",
        help="Numéro de facture, note de frais, etc.",
    )
    description = fields.Char("Description")
    etat = fields.Selection(
        [
            ("engage", "Engagé"),
            ("commande", "Commandé"),
            ("en_attente_paiement", "En attente paiement"),
            ("paye", "Payé"),
            ("annule", "Annulé"),
            ("conteste", "Contesté"),
        ],
        string="État",
        default="engage",
        required=True,
    )
    justificatif_attachment = fields.Boolean(
        "Justificatif joint",
        help="Cocher si un justificatif est attaché au document lié.",
    )
