# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

import re
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CoyaFicheChamp(models.Model):
    _name = "coya.fiche.champ"
    _description = "Champ de fiche modulable"
    _order = "sequence, id"

    name = fields.Char("Libellé", required=True)
    technical_name = fields.Char("Nom technique", compute="_compute_technical_name", store=True, readonly=False)
    fiche_type_id = fields.Many2one("coya.fiche.type", string="Type de fiche", required=True, ondelete="cascade")
    champ_type = fields.Selection(
        [
            ("char", "Texte court"),
            ("text", "Texte long"),
            ("integer", "Nombre entier"),
            ("float", "Nombre décimal"),
            ("date", "Date"),
            ("datetime", "Date et heure"),
            ("selection", "Liste déroulante"),
            ("boolean", "Oui/Non"),
            ("email", "E-mail"),
            ("phone", "Téléphone"),
        ],
        string="Type",
        required=True,
        default="char",
    )
    selection_options = fields.Text("Options (une par ligne)", help="Pour type Liste : une valeur par ligne")
    required = fields.Boolean("Requis", default=False)
    sequence = fields.Integer("Ordre", default=10)

    @api.depends("name")
    def _compute_technical_name(self):
        for rec in self:
            if rec.name:
                base = re.sub(r"[^a-zA-Z0-9_]", "_", rec.name.lower()).strip("_")
                rec.technical_name = base or ("champ_%s" % rec.id if rec.id else "champ")
            else:
                rec.technical_name = ""
