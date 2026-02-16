# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError


class CoyaPayslip(models.Model):
    _name = "coya.payslip"
    _description = "Bulletin de paie COYA"
    _order = "date_from desc"

    name = fields.Char("Libellé", compute="_compute_name", store=True)
    employee_id = fields.Many2one(
        "hr.employee",
        string="Employé",
        required=True,
        ondelete="cascade",
    )
    contract_id = fields.Many2one(
        "hr.contract",
        string="Contrat",
        ondelete="restrict",
    )
    date_from = fields.Date("Début période", required=True)
    date_to = fields.Date("Fin période", required=True)
    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("done", "Validé"),
            ("cancel", "Annulé"),
        ],
        default="draft",
    )
    line_ids = fields.One2many(
        "coya.payslip.line",
        "payslip_id",
        string="Lignes",
    )
    company_id = fields.Many2one(
        "res.company",
        related="employee_id.company_id",
        store=True,
    )
    # Montants calculés (pour affichage)
    total_brut = fields.Float("Total brut", digits="Account", compute="_compute_totals", store=True)
    total_cotisations = fields.Float("Cotisations", digits="Account", compute="_compute_totals", store=True)
    total_retenues = fields.Float("Retenues", digits="Account", compute="_compute_totals", store=True)
    total_net = fields.Float("Net à payer", digits="Account", compute="_compute_totals", store=True)

    @api.depends("employee_id", "date_from", "date_to")
    def _compute_name(self):
        for p in self:
            if p.employee_id and p.date_from and p.date_to:
                p.name = "%s - %s / %s" % (p.employee_id.name, p.date_from, p.date_to)
            else:
                p.name = "Bulletin"

    @api.depends("line_ids", "line_ids.amount", "line_ids.category")
    def _compute_totals(self):
        for p in self:
            brut = cotisations = retenues = 0.0
            for line in p.line_ids:
                if line.category == "brut":
                    brut += line.amount
                elif line.category == "cotisation":
                    cotisations += line.amount
                elif line.category == "retenue":
                    retenues += line.amount
            p.total_brut = brut
            p.total_cotisations = cotisations
            p.total_retenues = retenues
            p.total_net = brut - cotisations - retenues

    def _get_contract(self):
        self.ensure_one()
        if self.contract_id:
            return self.contract_id
        contract = self.env["hr.contract"].search([
            ("employee_id", "=", self.employee_id.id),
            ("state", "in", ["open", "draft"]),
            "|",
            ("date_end", "=", False),
            ("date_end", ">=", self.date_to),
        ], limit=1)
        return contract

    def _get_hours_worked(self):
        """Heures pointées (présence) sur la période."""
        self.ensure_one()
        days = self.env["coya.presence.day"].search([
            ("employee_id", "=", self.employee_id.id),
            ("date", ">=", self.date_from),
            ("date", "<=", self.date_to),
        ])
        return sum(days.mapped("hours_worked"))

    def _get_hours_deficit(self):
        """Heures manquantes par rapport à 44 h/semaine (défalcation)."""
        self.ensure_one()
        emp = self.employee_id
        if not emp.presence_policy_apply:
            return 0.0
        target_weekly = emp.presence_heures_cibles_semaine or emp.company_id.presence_heures_cibles_semaine or 44.0
        weeks = max(1, (self.date_to - self.date_from).days / 7.0)
        target_total = target_weekly * weeks
        hours_worked = self._get_hours_worked()
        return max(0.0, target_total - hours_worked)

    def _get_sanctions_amount(self):
        """Montant total des sanctions présence sur la période."""
        self.ensure_one()
        sanctions = self.env["coya.presence.sanction"].search([
            ("employee_id", "=", self.employee_id.id),
            ("date", ">=", self.date_from),
            ("date", "<=", self.date_to),
        ])
        return sum(sanctions.mapped("montant"))

    def _get_trinite_prime(self):
        """Prime basée sur les scores Trinité de la période (Ndiguel, Barké, Yar)."""
        self.ensure_one()
        Score = self.env["coya.trinite.score"]
        score = Score.search([
            ("employee_id", "=", self.employee_id.id),
            ("periode_start", "<=", self.date_to),
            ("periode_end", ">=", self.date_from),
        ], order="periode_end desc", limit=1)
        if not score:
            return 0.0
        # Formule simple : moyenne des 3 scores en % d'un bonus (ex. 5 % du brut)
        avg = (score.score_ndiguel + score.score_barke + score.score_yar) / 3.0
        # À paramétrer : % du brut ou montant fixe par tranche de score
        contract = self._get_contract()
        if not contract or not hasattr(contract, "wage"):
            return 0.0
        wage = getattr(contract, "wage", 0) or 0
        # Prime = jusqu'à 5 % du salaire selon score (0-100 → 0-5 %)
        prime_pct = (avg / 100.0) * 0.05
        return wage * prime_pct

    def action_compute(self):
        """Calcule les lignes du bulletin."""
        for slip in self:
            if slip.state != "draft":
                raise UserError("Seul un bulletin brouillon peut être calculé.")
            slip.line_ids.unlink()
            contract = slip._get_contract()
            if not contract:
                raise UserError("Aucun contrat trouvé pour cet employé sur la période.")
            wage = getattr(contract, "wage", 0) or 0
            hourly_rate = getattr(contract, "hourly_rate", 0) or (wage / 173.33 if wage else 0)
            wage_type = getattr(contract, "wage_type", "monthly") or "monthly"

            lines_vals = []

            # Brut de base
            hours_worked = slip._get_hours_worked()
            if wage_type == "hourly" and hourly_rate:
                brut_base = hours_worked * hourly_rate
            else:
                # Mensuel : prorata ou plein selon période
                days_in_month = 30
                brut_base = wage  # simplifié : plein mois

            lines_vals.append({
                "payslip_id": slip.id,
                "code": "BRUT",
                "name": "Salaire de base",
                "category": "brut",
                "amount": brut_base,
            })

            # Défalcation (heures manquantes)
            deficit = slip._get_hours_deficit()
            if deficit and slip.employee_id.company_id.presence_appliquer_defalcation:
                defalcation = deficit * hourly_rate
                lines_vals.append({
                    "payslip_id": slip.id,
                    "code": "DEFALC",
                    "name": "Défalcation heures insuffisantes",
                    "category": "retenue",
                    "amount": -defalcation,
                })

            # Sanctions
            sanction_amount = slip._get_sanctions_amount()
            if sanction_amount:
                lines_vals.append({
                    "payslip_id": slip.id,
                    "code": "SANCTION",
                    "name": "Sanctions présence",
                    "category": "retenue",
                    "amount": -sanction_amount,
                })

            # Prime Trinité
            trinite_prime = slip._get_trinite_prime()
            if trinite_prime:
                lines_vals.append({
                    "payslip_id": slip.id,
                    "code": "PRIME_TRINITE",
                    "name": "Prime performance / qualité (Trinité)",
                    "category": "brut",
                    "amount": trinite_prime,
                })

            # Cotisations (structure simplifiée - à compléter selon droit sénégalais)
            company = slip.company_id
            brut_for_cotisations = brut_base + trinite_prime
            if getattr(company, "cnss_employee_rate", 0):
                cnss = brut_for_cotisations * (company.cnss_employee_rate / 100.0)
                lines_vals.append({
                    "payslip_id": slip.id,
                    "code": "CNSS",
                    "name": "CNSS (part salariale)",
                    "category": "cotisation",
                    "amount": -cnss,
                })
            if getattr(company, "amo_rate", 0):
                amo = brut_for_cotisations * (company.amo_rate / 100.0)
                lines_vals.append({
                    "payslip_id": slip.id,
                    "code": "AMO",
                    "name": "AMO",
                    "category": "cotisation",
                    "amount": -amo,
                })
            if getattr(company, "mutuelle_employee", 0):
                lines_vals.append({
                    "payslip_id": slip.id,
                    "code": "MUTUELLE",
                    "name": "Mutuelle",
                    "category": "cotisation",
                    "amount": -company.mutuelle_employee,
                })

            self.env["coya.payslip.line"].create(lines_vals)
        return True

    def action_validate(self):
        for slip in self:
            if slip.state != "draft":
                raise UserError("Seul un bulletin brouillon peut être validé.")
            slip.state = "done"
        return True

    def action_cancel(self):
        for slip in self:
            slip.state = "cancel"
        return True

    def action_draft(self):
        for slip in self:
            if slip.state != "cancel":
                raise UserError("Seul un bulletin annulé peut être remis en brouillon.")
            slip.state = "draft"
        return True


class CoyaPayslipLine(models.Model):
    _name = "coya.payslip.line"
    _description = "Ligne de bulletin de paie"

    payslip_id = fields.Many2one(
        "coya.payslip",
        string="Bulletin",
        required=True,
        ondelete="cascade",
    )
    code = fields.Char("Code", required=True)
    name = fields.Char("Libellé", required=True)
    category = fields.Selection(
        [
            ("brut", "Brut"),
            ("cotisation", "Cotisation"),
            ("retenue", "Retenue"),
        ],
        string="Catégorie",
        required=True,
    )
    amount = fields.Float("Montant", digits="Account", required=True)
