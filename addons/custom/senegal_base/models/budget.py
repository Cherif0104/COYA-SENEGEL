from odoo import api, fields, models


class CoyaBudget(models.Model):
    """Ligne de budget simple pour un projet / département / axe Trinité."""

    _name = "coya.budget"
    _description = "COYA Budget"

    name = fields.Char("Libellé", required=True)
    date_from = fields.Date("Du", required=True)
    date_to = fields.Date("Au", required=True)

    project_id = fields.Many2one("project.project", string="Projet")
    department_id = fields.Many2one("hr.department", string="Département")

    coya_axis = fields.Selection(
        [
            ("ndiguel", "Productivité (Ndiguel)"),
            ("barke", "Profitabilité (Yéene)"),
            ("yar", "Professionnalisme (Yar)"),
        ],
        string="Axe Trinité",
        required=True,
    )

    analytic_account_id = fields.Many2one(
        "account.analytic.account",
        string="Compte analytique",
        help="Permet de lier le budget aux écritures analytiques correspondantes.",
    )

    amount_planned = fields.Monetary("Budget prévu", currency_field="currency_id", required=True)
    amount_spent = fields.Monetary("Réalisé", currency_field="currency_id", compute="_compute_amounts", store=False)
    amount_remaining = fields.Monetary("Reste à consommer", currency_field="currency_id", compute="_compute_amounts", store=False)
    percent_used = fields.Float("% consommé", compute="_compute_amounts", store=False)

    currency_id = fields.Many2one(
        "res.currency",
        string="Devise",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )

    alert_threshold = fields.Float(
        "Seuil d'alerte (%)",
        default=80.0,
        help="Un avertissement est généré si le pourcentage consommé dépasse ce seuil.",
    )

    active = fields.Boolean(default=True)

    @api.depends("amount_planned", "analytic_account_id", "date_from", "date_to")
    def _compute_amounts(self):
        account_move_line = self.env.get("account.move.line")
        for record in self:
            spent = 0.0
            if (
                account_move_line
                and record.analytic_account_id
                and record.date_from
                and record.date_to
            ):
                domain = [
                    ("analytic_account_id", "=", record.analytic_account_id.id),
                    ("date", ">=", record.date_from),
                    ("date", "<=", record.date_to),
                ]
                lines = account_move_line.search(domain)
                spent = sum(lines.mapped("balance"))

            record.amount_spent = spent
            record.amount_remaining = record.amount_planned - spent
            record.percent_used = (
                spent / record.amount_planned * 100.0 if record.amount_planned else 0.0
            )

    def action_check_alert(self):
        """Vérifie les seuils et crée des activités sur les budgets en dépassement."""
        MailActivity = self.env.get("mail.activity")
        for budget in self:
            if budget.percent_used >= budget.alert_threshold and MailActivity:
                existing = MailActivity.search(
                    [
                        ("res_model", "=", budget._name),
                        ("res_id", "=", budget.id),
                        ("activity_type_id", "=", self.env.ref("mail.mail_activity_data_warning").id),
                    ],
                    limit=1,
                )
                if existing:
                    continue

                MailActivity.create(
                    {
                        "res_model": budget._name,
                        "res_id": budget.id,
                        "activity_type_id": self.env.ref("mail.mail_activity_data_warning").id,
                        "user_id": self.env.user.id,
                        "summary": "Budget au-dessus du seuil",
                        "note": (
                            f"Le budget {budget.name} a consommé {budget.percent_used:.1f}% "
                            f"du montant prévu (seuil {budget.alert_threshold:.1f}%)."
                        ),
                    }
                )

