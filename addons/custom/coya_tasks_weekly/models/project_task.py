# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    task_type = fields.Selection(
        [
            ("hebdo_partagee", "Hebdomadaire partagée"),
            ("journaliere", "Journalière"),
            ("projet", "Liée projet / programme"),
            ("autre", "Autre"),
        ],
        string="Type de tâche",
        default="autre",
    )
    objectif_smart = fields.Text(
        "Objectif SMART",
        help="Objectif Spécifique, Mesurable, Atteignable, Réaliste, Temporellement défini.",
    )
    date_limite = fields.Date(
        "Date limite",
        help="Limite semaine ou jour selon le type.",
    )
    livree = fields.Boolean(
        "Livrée (point hebdo)",
        default=False,
        help="Coché lors du point hebdomadaire si la tâche est livrée.",
    )
    coya_projet_id = fields.Many2one(
        "coya.projet",
        string="Projet / Programme",
        ondelete="set null",
        help="Projet ou programme (financement externe) lié à cette tâche.",
    )
    coya_programme_id = fields.Many2one(
        "coya.programme",
        related="coya_projet_id.programme_id",
        string="Programme",
        store=True,
    )

    @api.model
    def action_open_week_tasks(self):
        """Ouvre la liste des tâches dont la date limite est dans la semaine courante."""
        today = fields.Date.context_today(self)
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        return {
            "type": "ir.actions.act_window",
            "name": "Tâches de la semaine",
            "res_model": "project.task",
            "view_mode": "list,form",
            "domain": [
                ("date_limite", ">=", week_start),
                ("date_limite", "<=", week_end),
            ],
            "context": {"default_task_type": "hebdo_partagee", "default_date_limite": week_end},
        }
