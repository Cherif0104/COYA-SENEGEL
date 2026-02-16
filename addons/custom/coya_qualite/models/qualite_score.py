# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CoyaQualiteScore(models.Model):
    _name = "coya.qualite.score"
    _description = "Score qualité global (période, département ou employé)"
    _order = "periode_end desc, department_key, employee_id"

    name = fields.Char("Libellé", compute="_compute_name", store=True)
    periode_start = fields.Date("Début période", required=True)
    periode_end = fields.Date("Fin période", required=True)
    department_key = fields.Selection(
        [
            ("admin", "Administratif & Financier"),
            ("juridique", "Juridique"),
            ("audiovisuel", "Audiovisuel"),
            ("formation", "Formation"),
            ("rh", "RH"),
            ("pm", "Project Management"),
            ("prospection", "Prospection"),
            ("conseil", "Conseil"),
            ("qualite", "Qualité"),
            ("it", "IT"),
        ],
        string="Département",
    )
    employee_id = fields.Many2one(
        "hr.employee",
        string="Employé",
        ondelete="set null",
    )
    score_global = fields.Float(
        "Score qualité global (0-100)",
        help="Agrégation des sources (Trinité, audits, contrôles).",
    )
    score_trinite = fields.Float(
        "Source Trinité (moyenne Ndiguel/Barké/Yar)",
        help="Moyenne des 3 piliers sur la période si employé renseigné.",
    )
    score_audits = fields.Float("Source Audits (0-100)")
    score_controles = fields.Float("Source Contrôles (0-100)")
    notes = fields.Text("Notes")

    @api.depends("periode_start", "periode_end", "department_key", "employee_id")
    def _compute_name(self):
        for rec in self:
            parts = ["%s → %s" % (rec.periode_start or "", rec.periode_end or "")]
            if rec.department_key:
                parts.append(dict(rec._fields["department_key"].selection).get(rec.department_key, ""))
            if rec.employee_id:
                parts.append(rec.employee_id.name)
            rec.name = " | ".join(filter(None, parts)) or "Score qualité"
