# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class HrAppraisal(models.Model):
    _inherit = "hr.appraisal"

    last_trinite_score_id = fields.Many2one(
        "coya.trinite.score",
        string="Dernier score Trinité",
        compute="_compute_last_trinite_score",
        store=False,
        readonly=True,
    )
    trinite_score_ndiguel = fields.Float(
        "Ndiguel (Productivité)",
        related="last_trinite_score_id.score_ndiguel",
        readonly=True,
    )
    trinite_score_barke = fields.Float(
        "Barké (Profitabilité)",
        related="last_trinite_score_id.score_barke",
        readonly=True,
    )
    trinite_score_yar = fields.Float(
        "Yar (Professionnalisme)",
        related="last_trinite_score_id.score_yar",
        readonly=True,
    )

    @api.depends("employee_id")
    def _compute_last_trinite_score(self):
        for rec in self:
            if rec.employee_id:
                last = (
                    rec.env["coya.trinite.score"]
                    .search(
                        [("employee_id", "=", rec.employee_id.id)],
                        order="periode_end desc",
                        limit=1,
                    )
                )
                rec.last_trinite_score_id = last
            else:
                rec.last_trinite_score_id = False
