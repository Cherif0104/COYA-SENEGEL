# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CoyaTrinitePlan(models.Model):
    _name = "coya.trinite.plan"
    _description = "Plan de paie conventionnel COYA"

    name = fields.Char("Nom", required=True)
    heures_base = fields.Float("Heures hebdomadaires type", default=40.0)
    description = fields.Text("Description / coefficients")
