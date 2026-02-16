# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CoyaAppraisalManager(models.Model):
    _name = "coya.appraisal.manager"
    _description = "Évaluation manager (supérieur + collaborateurs anonymes)"
    _order = "period_end desc, employee_id"

    employee_id = fields.Many2one(
        "hr.employee",
        string="Manager évalué",
        required=True,
        ondelete="cascade",
    )
    period_start = fields.Date("Début période", required=True)
    period_end = fields.Date("Fin période", required=True)
    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("in_progress", "En cours (saisie collaborateurs)"),
            ("done", "Clôturé"),
        ],
        default="draft",
    )
    # Part supérieur (50–60 %)
    weight_superior = fields.Float(
        "Pondération supérieur (%)",
        default=55.0,
        help="Part de la note du supérieur dans la note finale (50–60 %).",
    )
    note_superior = fields.Float(
        "Note supérieur",
        digits=(3, 2),
        help="Note saisie par le supérieur hiérarchique.",
    )
    comment_superior = fields.Text("Commentaire supérieur")
    # Part collaborateurs (40–50 %)
    weight_collaborators = fields.Float(
        "Pondération collaborateurs (%)",
        default=45.0,
        compute="_compute_weight_collaborators",
        store=True,
    )
    response_ids = fields.One2many(
        "coya.appraisal.manager.response",
        "appraisal_id",
        string="Réponses collaborateurs (anonymes)",
    )
    note_collaborators_avg = fields.Float(
        "Note moyenne collaborateurs",
        digits=(3, 2),
        compute="_compute_note_collaborators",
        store=True,
    )
    note_final = fields.Float(
        "Note finale",
        digits=(3, 2),
        compute="_compute_note_final",
        store=True,
    )
    company_id = fields.Many2one(
        "res.company",
        related="employee_id.company_id",
        store=True,
    )

    @api.depends("weight_superior")
    def _compute_weight_collaborators(self):
        for rec in self:
            rec.weight_collaborators = 100.0 - rec.weight_superior

    @api.depends("response_ids", "response_ids.note")
    def _compute_note_collaborators(self):
        for rec in self:
            if not rec.response_ids:
                rec.note_collaborators_avg = 0.0
            else:
                rec.note_collaborators_avg = sum(rec.response_ids.mapped("note")) / len(rec.response_ids)

    @api.depends("note_superior", "note_collaborators_avg", "weight_superior", "weight_collaborators")
    def _compute_note_final(self):
        for rec in self:
            s = (rec.note_superior or 0) * (rec.weight_superior / 100.0)
            c = (rec.note_collaborators_avg or 0) * (rec.weight_collaborators / 100.0)
            rec.note_final = s + c

    def action_start_collect(self):
        """Passe en cours : ouverture des réponses collaborateurs."""
        for rec in self:
            if rec.state != "draft":
                continue
            rec.state = "in_progress"
        return True

    def action_done(self):
        for rec in self:
            rec.state = "done"
        return True


class CoyaAppraisalManagerResponse(models.Model):
    _name = "coya.appraisal.manager.response"
    _description = "Réponse anonyme d'un collaborateur (évaluation manager)"

    appraisal_id = fields.Many2one(
        "coya.appraisal.manager",
        string="Évaluation",
        required=True,
        ondelete="cascade",
    )
    note = fields.Float("Note", digits=(3, 2), required=True)
    comment = fields.Text("Commentaire (optionnel)")
    # Pas de champ évaluateur : 100 % anonyme
