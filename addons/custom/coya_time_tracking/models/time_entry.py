# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CoyaTimeEntry(models.Model):
    _name = "coya.time.entry"
    _description = "Entrée de temps COYA"
    _order = "date_start desc"

    employee_id = fields.Many2one(
        "hr.employee",
        string="Employé",
        required=True,
        ondelete="cascade",
    )
    date = fields.Date("Date", required=True, index=True)
    date_start = fields.Datetime("Début", required=True)
    date_stop = fields.Datetime("Fin", required=True)
    unit_amount = fields.Float("Durée (heures)", compute="_compute_unit_amount", store=True, readonly=False)
    activity_type = fields.Selection(
        [
            ("production", "Production"),
            ("reunion", "Réunion"),
            ("formation", "Formation"),
            ("terrain", "Terrain"),
            ("teletravail", "Télétravail"),
            ("autre", "Autre"),
        ],
        string="Type d'activité",
        default="production",
        required=True,
    )
    project_id = fields.Many2one(
        "project.project",
        string="Projet",
        ondelete="set null",
    )
    task_id = fields.Many2one(
        "project.task",
        string="Tâche",
        ondelete="set null",
    )
    planning_slot_id = fields.Many2one(
        "coya.planning.slot",
        string="Créneau planifié",
        ondelete="set null",
    )
    notes = fields.Text("Notes")

    @api.depends("date_start", "date_stop")
    def _compute_unit_amount(self):
        for entry in self:
            if entry.date_start and entry.date_stop:
                delta = entry.date_stop - entry.date_start
                entry.unit_amount = delta.total_seconds() / 3600.0
            else:
                entry.unit_amount = 0.0

    @api.constrains("date_start", "date_stop")
    def _check_dates(self):
        for entry in self:
            if entry.date_start and entry.date_stop and entry.date_stop <= entry.date_start:
                raise ValidationError("La date de fin doit être postérieure à la date de début.")

    @api.onchange("date_start", "date_stop")
    def _onchange_date(self):
        if self.date_start:
            self.date = self.date_start.date()
