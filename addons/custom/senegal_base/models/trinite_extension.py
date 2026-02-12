from odoo import fields, models


class HrEmployeeTrinite(models.Model):
    _inherit = "hr.employee"

    coya_trinite_axis = fields.Selection(
        [
            ("ndiguel", "Productivité (Ndiguel)"),
            ("barke", "Profitabilité (Yéene)"),
            ("yar", "Professionnalisme (Yar)"),
        ],
        string="Axe Trinité principal",
        help="Axe principal de contribution de cet employé.",
    )
    coya_trinite_score = fields.Float(
        string="Score Trinité global",
        help="Score qualitatif global de la Trinité pour cet employé (0–100).",
    )


class ProjectTrinite(models.Model):
    _inherit = "project.project"

    coya_trinite_axis = fields.Selection(
        [
            ("ndiguel", "Productivité (Ndiguel)"),
            ("barke", "Profitabilité (Yéene)"),
            ("yar", "Professionnalisme (Yar)"),
        ],
        string="Axe Trinité",
        help="Axe de la Trinité principalement visé par ce projet.",
    )
    coya_trinite_score_ndiguel = fields.Float(string="Score Ndiguel", help="Score de productivité pour ce projet.")
    coya_trinite_score_barke = fields.Float(string="Score Yéene", help="Score de profitabilité pour ce projet.")
    coya_trinite_score_yar = fields.Float(string="Score Yar", help="Score de professionnalisme pour ce projet.")


class AnalyticAccountTrinite(models.Model):
    _inherit = "account.analytic.account"

    coya_trinite_axis = fields.Selection(
        [
            ("ndiguel", "Productivité (Ndiguel)"),
            ("barke", "Profitabilité (Yéene)"),
            ("yar", "Professionnalisme (Yar)"),
        ],
        string="Axe Trinité",
        help="Axe de la Trinité associé à ce centre de coûts.",
    )

