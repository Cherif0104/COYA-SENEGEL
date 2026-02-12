from odoo import api, fields, models


class CoyaDashboard(models.Model):
    """Modèle simple pour agréger quelques KPIs globaux.

    On reste volontairement léger : si certains modules (hr, project, account)
    ne sont pas installés, les indicateurs restent simplement à 0.
    """

    _name = "coya.dashboard"
    _description = "COYA.PRO Dashboard"

    name = fields.Char(default="COYA Dashboard")

    total_employee_count = fields.Integer(string="Employés", compute="_compute_metrics", store=False)
    total_project_count = fields.Integer(string="Projets", compute="_compute_metrics", store=False)
    open_task_count = fields.Integer(string="Tâches ouvertes", compute="_compute_metrics", store=False)
    open_invoice_count = fields.Integer(string="Factures ouvertes", compute="_compute_metrics", store=False)

    trinite_productivite = fields.Float(string="Productivité (Ndiguel)", compute="_compute_trinite", store=False)
    trinite_profitabilite = fields.Float(string="Profitabilité (Barké)", compute="_compute_trinite", store=False)
    trinite_professionnalisme = fields.Float(string="Professionnalisme (Yar)", compute="_compute_trinite", store=False)

    @api.model
    def create(self, vals):
        """Forcer un seul enregistrement (singleton) pour le dashboard."""
        if self.search([], limit=1):
            # Toujours retourner le premier dashboard existant
            return self.search([], limit=1)
        return super().create(vals)

    @api.model
    def get_singleton(self):
        """Utilitaire pour obtenir (ou créer) l'unique enregistrement."""
        dashboard = self.search([], limit=1)
        if not dashboard:
            dashboard = self.create({})
        return dashboard

    @api.depends()
    def _compute_metrics(self):
        for record in self:
            # Employés
            hr_employee = self.env.get("hr.employee")
            record.total_employee_count = hr_employee.search_count([]) if hr_employee else 0

            # Projets
            project_project = self.env.get("project.project")
            record.total_project_count = project_project.search_count([]) if project_project else 0

            # Tâches ouvertes
            project_task = self.env.get("project.task")
            if project_task:
                record.open_task_count = project_task.search_count(
                    [("stage_id.fold", "=", False)]
                )
            else:
                record.open_task_count = 0

            # Factures clients ouvertes
            account_move = self.env.get("account.move")
            if account_move and "state" in account_move._fields:
                record.open_invoice_count = account_move.search_count(
                    [("move_type", "in", ["out_invoice", "out_refund"]), ("state", "=", "posted")]
                )
            else:
                record.open_invoice_count = 0

    @api.depends()
    def _compute_trinite(self):
        """Version très simple : dérive la Trinité à partir d'indicateurs existants.

        L'idée est d'avoir un socle que l'on pourra raffiner ensuite :
        - Productivité : proportion de tâches clôturées vs totales.
        - Profitabilité : ratio factures payées vs totales (si dispo).
        - Professionnalisme : ratio d'employés actifs vs total (proxy).
        """
        project_task = self.env.get("project.task")
        account_move = self.env.get("account.move")
        hr_employee = self.env.get("hr.employee")

        for record in self:
            # Productivité (tâches clôturées / toutes tâches)
            if project_task:
                total_tasks = project_task.search_count([])
                done_tasks = project_task.search_count([("stage_id.fold", "=", True)])
                record.trinite_productivite = (done_tasks / total_tasks * 100.0) if total_tasks else 0.0
            else:
                record.trinite_productivite = 0.0

            # Profitabilité (factures payées / factures postées)
            if account_move and {"payment_state", "state"}.issubset(account_move._fields):
                posted_invoices = account_move.search_count(
                    [("move_type", "in", ["out_invoice", "out_refund"]), ("state", "=", "posted")]
                )
                paid_invoices = account_move.search_count(
                    [
                        ("move_type", "in", ["out_invoice", "out_refund"]),
                        ("state", "=", "posted"),
                        ("payment_state", "=", "paid"),
                    ]
                )
                record.trinite_profitabilite = (
                    paid_invoices / posted_invoices * 100.0 if posted_invoices else 0.0
                )
            else:
                record.trinite_profitabilite = 0.0

            # Professionnalisme (employés actifs / tous les employés)
            if hr_employee and "active" in hr_employee._fields:
                total_emp = hr_employee.with_context(active_test=False).search_count([])
                active_emp = hr_employee.search_count([("active", "=", True)])
                record.trinite_professionnalisme = (
                    active_emp / total_emp * 100.0 if total_emp else 0.0
                )
            else:
                record.trinite_professionnalisme = 0.0

