# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    presence_policy_apply = fields.Boolean(
        "Politique de présence applicable",
        default=True,
        help="Si coché, les règles 44 h/semaine, plafond 10 h/jour et défalcation s'appliquent à cet employé.",
    )
    presence_heures_cibles_semaine = fields.Float(
        "Heures cibles par semaine (override)",
        help="Laissez vide pour utiliser la valeur société.",
    )
    presence_plafond_heures_jour = fields.Float(
        "Plafond heures par jour (override)",
        help="Laissez vide pour utiliser la valeur société.",
    )
