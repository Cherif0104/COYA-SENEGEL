# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CoyaFicheType(models.Model):
    _name = "coya.fiche.type"
    _description = "Type de fiche de collecte"

    name = fields.Char("Nom", required=True)
    description = fields.Text("Description")
    active = fields.Boolean("Actif", default=True)
    champ_ids = fields.One2many(
        "coya.fiche.champ",
        "fiche_type_id",
        string="Champs",
        copy=True,
    )
    reponse_ids = fields.One2many(
        "coya.fiche.reponse",
        "fiche_type_id",
        string="Réponses",
        readonly=True,
    )
    reponse_count = fields.Integer(compute="_compute_reponse_count", string="Nombre de réponses")
    public_url = fields.Char(compute="_compute_public_url", string="Lien public")

    def _compute_public_url(self):
        for rec in self:
            base = rec.env["ir.config_parameter"].sudo().get_param("web.base.url", "http://localhost:8069")
            rec.public_url = f"{base.rstrip('/')}/coya/fiche/{rec.id}"

    def _compute_reponse_count(self):
        for rec in self:
            rec.reponse_count = len(rec.reponse_ids)
