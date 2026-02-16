# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CoyaLigneBudgetaire(models.Model):
    _name = "coya.ligne.budgetaire"
    _description = "Ligne budgétaire (poste par projet)"
    _order = "projet_id, name"

    name = fields.Char("Poste / Nature", required=True)
    projet_id = fields.Many2one(
        "coya.projet",
        string="Projet",
        required=True,
        ondelete="cascade",
    )
    programme_id = fields.Many2one(
        "coya.programme",
        related="projet_id.programme_id",
        store=True,
    )
    montant_previsionnel = fields.Monetary(
        "Montant prévisionnel",
        required=True,
        currency_field="currency_id",
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="projet_id.currency_id",
        store=True,
    )
    imputation_ids = fields.One2many(
        "coya.imputation.depense",
        "ligne_budgetaire_id",
        string="Imputations",
    )
    montant_engage = fields.Monetary(
        "Engagé",
        compute="_compute_montants",
        currency_field="currency_id",
        store=True,
    )
    montant_paye = fields.Monetary(
        "Payé",
        compute="_compute_montants",
        currency_field="currency_id",
        store=True,
    )
    montant_restant = fields.Monetary(
        "Restant",
        compute="_compute_montants",
        currency_field="currency_id",
        store=True,
    )

    @api.depends("imputation_ids.montant", "imputation_ids.etat", "montant_previsionnel")
    def _compute_montants(self):
        for line in self:
            imputations = line.imputation_ids
            line.montant_engage = sum(imputations.mapped("montant"))
            line.montant_paye = sum(
                imputations.filtered(lambda i: i.etat == "paye").mapped("montant")
            )
            line.montant_restant = line.montant_previsionnel - line.montant_engage

    @api.constrains("imputation_ids", "montant_previsionnel")
    def _check_depassement(self):
        for rec in self:
            if rec.montant_engage > rec.montant_previsionnel:
                raise ValidationError(
                    "Le total des imputations (%.2f) dépasse le montant prévisionnel (%.2f) de la ligne « %s »."
                    % (rec.montant_engage, rec.montant_previsionnel, rec.name)
                )
