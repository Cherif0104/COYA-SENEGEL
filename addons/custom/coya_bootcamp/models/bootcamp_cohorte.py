# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CoyaBootcampCohorte(models.Model):
    _name = "coya.bootcamp.cohorte"
    _description = "Cohorte / Session de bootcamp"
    _order = "date_start desc"

    name = fields.Char("Nom", required=True)
    bootcamp_id = fields.Many2one(
        "coya.bootcamp",
        string="Bootcamp",
        required=True,
        ondelete="cascade",
    )
    date_start = fields.Date("Début")
    date_end = fields.Date("Fin")
    location = fields.Char("Lieu / Région")
    state = fields.Selection(
        [
            ("draft", "Prévue"),
            ("brouillon", "Brouillon"),
            ("recrutement", "Recrutement"),
            ("ongoing", "En cours"),
            ("suspension", "Suspension"),
            ("done", "Terminée"),
            ("cloturee", "Clôturée"),
            ("cancelled", "Annulée"),
        ],
        string="État",
        default="draft",
        required=True,
    )
    intervenant_ids = fields.One2many(
        "coya.bootcamp.intervenant",
        "cohorte_id",
        string="Intervenants",
    )
    participant_ids = fields.One2many(
        "coya.bootcamp.participant",
        "cohorte_id",
        string="Participants",
    )
