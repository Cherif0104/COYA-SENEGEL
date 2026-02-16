# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CoyaProjet(models.Model):
    _inherit = "coya.projet"

    project_id = fields.Many2one(
        "project.project",
        string="Projet Odoo (tâches)",
        ondelete="set null",
        help="Lien vers le projet planning Odoo.",
    )
