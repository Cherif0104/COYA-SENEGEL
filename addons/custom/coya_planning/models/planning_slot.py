# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CoyaPlanningSlot(models.Model):
    _name = "coya.planning.slot"
    _description = "Créneau de planification COYA"
    _order = "date_start desc"

    name = fields.Char("Libellé", required=True)
    employee_id = fields.Many2one(
        "hr.employee",
        string="Employé",
        required=True,
        ondelete="cascade",
    )
    slot_type = fields.Selection(
        [
            ("reunion", "Réunion"),
            ("teletravail", "Télétravail"),
            ("bureau", "Bureau"),
            ("terrain", "Intervention terrain"),
            ("formation", "Formation"),
            ("conge", "Congé / Absence"),
            ("modulation", "Modulation horaire"),
            ("autre", "Autre"),
        ],
        string="Type",
        required=True,
        default="bureau",
    )
    date_start = fields.Datetime("Début", required=True)
    date_stop = fields.Datetime("Fin", required=True)
    location = fields.Char("Lieu / Adresse")
    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("confirmed", "Confirmé"),
            ("en_cours", "En cours"),
            ("done", "Terminé"),
            ("reporte", "Reporté"),
            ("cancelled", "Annulé"),
        ],
        string="État",
        default="draft",
        required=True,
    )
    notes = fields.Text("Notes")

    @api.constrains("date_start", "date_stop")
    def _check_dates(self):
        for slot in self:
            if slot.date_start and slot.date_stop and slot.date_stop <= slot.date_start:
                raise ValidationError("La date de fin doit être postérieure à la date de début.")
