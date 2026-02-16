# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CoyaProgramme(models.Model):
    _name = "coya.programme"
    _description = "Programme (bailleur / financeur)"
    _order = "date_start desc, name"

    name = fields.Char("Nom du programme", required=True)
    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("active", "Actif"),
            ("closed", "Clôturé"),
            ("archived", "Archivé"),
        ],
        string="État",
        default="draft",
        required=True,
    )
    bailleur_id = fields.Many2one(
        "res.partner",
        string="Bailleur / Financeur",
        ondelete="restrict",
    )
    date_start = fields.Date("Début")
    date_end = fields.Date("Fin")
    description = fields.Text("Description")
    projet_ids = fields.One2many(
        "coya.projet",
        "programme_id",
        string="Projets",
    )
    montant_total_previsionnel = fields.Monetary(
        "Montant total prévisionnel",
        compute="_compute_montants",
        currency_field="currency_id",
        store=True,
    )
    montant_engage = fields.Monetary(
        "Total engagé",
        compute="_compute_montants",
        currency_field="currency_id",
        store=True,
    )
    montant_paye = fields.Monetary(
        "Total payé",
        compute="_compute_montants",
        currency_field="currency_id",
        store=True,
    )
    montant_restant = fields.Monetary(
        "Total restant",
        compute="_compute_montants",
        currency_field="currency_id",
        store=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Devise",
        default=lambda self: self.env.company.currency_id,
    )

    @api.depends(
        "projet_ids",
        "projet_ids.montant_total_previsionnel",
        "projet_ids.montant_engage",
        "projet_ids.montant_paye",
        "projet_ids.montant_restant",
    )
    def _compute_montants(self):
        for rec in self:
            rec.montant_total_previsionnel = sum(
                rec.projet_ids.mapped("montant_total_previsionnel")
            )
            rec.montant_engage = sum(rec.projet_ids.mapped("montant_engage"))
            rec.montant_paye = sum(rec.projet_ids.mapped("montant_paye"))
            rec.montant_restant = sum(rec.projet_ids.mapped("montant_restant"))
