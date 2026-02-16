# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CoyaPresenceSanction(models.Model):
    _name = "coya.presence.sanction"
    _description = "Sanction présence (3e retard / absence non justifiée)"
    _order = "date desc, employee_id"

    employee_id = fields.Many2one(
        "hr.employee",
        string="Employé",
        required=True,
        ondelete="cascade",
        index=True,
    )
    date = fields.Date("Date", required=True, index=True)
    type_sanction = fields.Selection(
        [
            ("retard", "Retard"),
            ("absence_non_autorisee", "Absence non autorisée"),
        ],
        string="Type",
        required=True,
    )
    presence_day_id = fields.Many2one(
        "coya.presence.day",
        string="Jour concerné",
        ondelete="set null",
    )
    montant = fields.Float(
        "Montant déduit",
        digits="Account",
        help="Montant ou valeur calculée (selon paramètre société) à déduire du salaire.",
    )
    company_id = fields.Many2one(
        "res.company",
        related="employee_id.company_id",
        store=True,
    )

    @api.model
    def _compute_sanction_amount(self, employee):
        """Calcule le montant de la sanction selon paramètres société."""
        company = employee.company_id
        if not company:
            return 0.0
        if company.presence_sanction_type == "fixe":
            return company.presence_sanction_montant or 0.0
        # pourcentage: on aura besoin du salaire brut (phase 5); pour l'instant on stocke le taux
        # et le montant sera calculé en paie. On stocke 0 ou on pourrait lier au contrat.
        return 0.0  # Sera calculé en paie à partir de presence_sanction_taux
