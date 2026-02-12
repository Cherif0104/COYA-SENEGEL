from odoo import api, fields, models


class CoyaJustificatif(models.Model):
    """Pièce justificative financière (facture, reçu, preuve de paiement…).

    Objectif : centraliser les scans et les lier aux pièces comptables.
    """

    _name = "coya.justificatif"
    _description = "COYA Pièce justificative"

    name = fields.Char("Référence", required=True)
    type = fields.Selection(
        [
            ("invoice", "Facture"),
            ("receipt", "Reçu"),
            ("payment_proof", "Preuve de paiement"),
            ("expense_note", "Note de frais"),
            ("other", "Autre"),
        ],
        string="Type",
        default="invoice",
        required=True,
    )
    amount = fields.Monetary("Montant", currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", string="Devise", required=True, default=lambda self: self.env.company.currency_id)
    date = fields.Date("Date du document", default=fields.Date.context_today)

    move_id = fields.Many2one(
        "account.move",
        string="Facture / écriture liée",
        domain="[('move_type', 'in', ('out_invoice','in_invoice','out_refund','in_refund'))]",
        help="Facture ou pièce comptable associée à ce justificatif.",
    )
    payment_id = fields.Many2one(
        "account.payment",
        string="Paiement lié",
        help="En cas de preuve de paiement spécifique.",
    )

    file = fields.Binary("Fichier scanné", attachment=True)
    filename = fields.Char("Nom du fichier")

    project_id = fields.Many2one("project.project", string="Projet")
    department_id = fields.Many2one("hr.department", string="Département")

    coya_axis = fields.Selection(
        [
            ("ndiguel", "Productivité (Ndiguel)"),
            ("barke", "Profitabilité (Yéene)"),
            ("yar", "Professionnalisme (Yar)"),
        ],
        string="Axe Trinité",
        help="Permet de rattacher ce justificatif à un axe de la Trinité.",
    )

    @api.depends("move_id", "payment_id")
    def _compute_display_name(self):
        super()._compute_display_name()

