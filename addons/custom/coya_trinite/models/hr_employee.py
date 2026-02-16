# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    trinite_score_ids = fields.One2many(
        "coya.trinite.score",
        "employee_id",
        string="Historique scores Trinité",
        readonly=True,
    )
    last_trinite_score_id = fields.Many2one(
        "coya.trinite.score",
        string="Dernier score Trinité",
        compute="_compute_last_trinite_score",
        store=False,
        readonly=True,
    )
    score_ndiguel = fields.Float(
        "Ndiguel (Productivité)",
        related="last_trinite_score_id.score_ndiguel",
        readonly=True,
    )
    score_barke = fields.Float(
        "Barké (Profitabilité)",
        related="last_trinite_score_id.score_barke",
        readonly=True,
    )
    score_yar = fields.Float(
        "Yar (Professionnalisme)",
        related="last_trinite_score_id.score_yar",
        readonly=True,
    )

    @api.depends("trinite_score_ids", "trinite_score_ids.periode_end")
    def _compute_last_trinite_score(self):
        for emp in self:
            last = emp.trinite_score_ids.sorted("periode_end", reverse=True)[:1]
            emp.last_trinite_score_id = last if last else False
