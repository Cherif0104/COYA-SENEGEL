# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CoyaProjet(models.Model):
    _name = "coya.projet"
    _description = "Projet (lié à un programme)"
    _order = "name"

    name = fields.Char("Nom du projet", required=True)
    programme_id = fields.Many2one(
        "coya.programme",
        string="Programme",
        required=True,
        ondelete="cascade",
    )
    date_start = fields.Date("Début")
    date_end = fields.Date("Fin")
    description = fields.Text("Description")
    ligne_budgetaire_ids = fields.One2many(
        "coya.ligne.budgetaire",
        "projet_id",
        string="Lignes budgétaires",
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="programme_id.currency_id",
        store=True,
    )
    montant_total_previsionnel = fields.Monetary(
        "Total prévisionnel",
        compute="_compute_montants",
        currency_field="currency_id",
        store=True,
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

    @api.depends("ligne_budgetaire_ids", "ligne_budgetaire_ids.montant_previsionnel",
                 "ligne_budgetaire_ids.montant_engage", "ligne_budgetaire_ids.montant_paye",
                 "ligne_budgetaire_ids.montant_restant")
    def _compute_montants(self):
        for rec in self:
            lines = rec.ligne_budgetaire_ids
            rec.montant_total_previsionnel = sum(lines.mapped("montant_previsionnel"))
            rec.montant_engage = sum(lines.mapped("montant_engage"))
            rec.montant_paye = sum(lines.mapped("montant_paye"))
            rec.montant_restant = sum(lines.mapped("montant_restant"))
