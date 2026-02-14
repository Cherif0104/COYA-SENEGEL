# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CoyaBootcampParticipant(models.Model):
    _name = "coya.bootcamp.participant"
    _description = "Participant (candidat, sélectionné, apprenant)"
    _order = "cohorte_id, state, name"

    cohorte_id = fields.Many2one(
        "coya.bootcamp.cohorte",
        string="Cohorte",
        required=True,
        ondelete="cascade",
    )
    name = fields.Char("Nom", required=True)
    email = fields.Char("E-mail")
    phone = fields.Char("Téléphone")
    partner_id = fields.Many2one(
        "res.partner",
        string="Contact lié",
        ondelete="set null",
    )
    fiche_reponse_id = fields.Many2one(
        "coya.fiche.reponse",
        string="Fiche de collecte",
        ondelete="set null",
        help="Réponse reçue via formulaire public",
    )
    state = fields.Selection(
        [
            ("candidat", "Candidat / Postulant"),
            ("selectionne", "Sélectionné"),
            ("apprenant", "Apprenant / En formation"),
            ("certifie", "Certifié"),
        ],
        string="Statut",
        required=True,
        default="candidat",
    )
    date_inscription = fields.Date("Date d'inscription", default=fields.Date.context_today)
    notes = fields.Text("Notes")
