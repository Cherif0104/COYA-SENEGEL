# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


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
            ("abandon", "Abandon"),
        ],
        string="Statut parcours",
        required=True,
        default="candidat",
    )
    date_inscription = fields.Date("Date d'inscription", default=fields.Date.context_today)
    date_certification = fields.Date(
        "Date de certification",
        help="Renseignée lorsque le statut passe à Certifié.",
    )
    notes = fields.Text("Notes")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("state") == "certifie" and not vals.get("date_certification"):
                vals["date_certification"] = fields.Date.context_today(self)
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("state") == "certifie":
            for rec in self:
                if not rec.date_certification:
                    vals.setdefault("date_certification", fields.Date.context_today(self))
                break
        return super().write(vals)
