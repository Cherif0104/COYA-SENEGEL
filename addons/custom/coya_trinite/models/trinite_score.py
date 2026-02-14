# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError

SEUIL_ALERTE = 30.0


class CoyaTriniteScore(models.Model):
    _name = "coya.trinite.score"
    _description = "Score Trinité par employé et période"
    _order = "periode_end desc, employee_id"

    employee_id = fields.Many2one(
        "hr.employee",
        string="Employé",
        required=True,
        ondelete="cascade",
    )
    periode_start = fields.Date("Début période", required=True)
    periode_end = fields.Date("Fin période", required=True)
    score_ndiguel = fields.Float("Ndiguel (Productivité)", default=0.0)
    score_barke = fields.Float("Barké (Profitabilité)", default=0.0)
    score_yar = fields.Float("Yar (Professionnalisme)", default=0.0)

    @api.constrains("periode_start", "periode_end")
    def _check_periode(self):
        for rec in self:
            if rec.periode_start and rec.periode_end and rec.periode_end < rec.periode_start:
                raise ValidationError("La fin de période doit être postérieure au début.")

    @api.constrains("score_ndiguel", "score_barke", "score_yar")
    def _check_scores(self):
        for rec in self:
            for val in [rec.score_ndiguel, rec.score_barke, rec.score_yar]:
                if val < 0 or val > 100:
                    raise ValidationError("Les scores doivent être entre 0 et 100.")

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._create_alertes_sous_seuil()
        return records

    def write(self, vals):
        res = super().write(vals)
        if any(k in vals for k in ("score_ndiguel", "score_barke", "score_yar")):
            self._create_alertes_sous_seuil()
        return res

    def _create_alertes_sous_seuil(self):
        """Crée des alertes Conseil quand un score est sous le seuil (30 %)."""
        Alerte = self.env["coya.trinite.alerte"]
        pilier_map = [
            ("ndiguel", "score_ndiguel"),
            ("barke", "score_barke"),
            ("yar", "score_yar"),
        ]
        for rec in self:
            for pilier, field in pilier_map:
                score = getattr(rec, field, 0) or 0
                if score < SEUIL_ALERTE:
                    existing = Alerte.search([
                        ("employee_id", "=", rec.employee_id.id),
                        ("pilier", "=", pilier),
                        ("state", "=", "open"),
                    ], limit=1)
                    if not existing:
                        Alerte.create({
                            "employee_id": rec.employee_id.id,
                            "pilier": pilier,
                            "score": score,
                            "seuil": SEUIL_ALERTE,
                            "state": "open",
                        })
