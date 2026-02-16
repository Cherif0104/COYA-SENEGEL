# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    presence_heures_cibles_semaine = fields.Float(
        "Heures cibles par semaine",
        default=44.0,
        help="Objectif hebdomadaire (ex. 44 h). Utilisé pour alerte et défalcation si activé.",
    )
    presence_plafond_heures_jour = fields.Float(
        "Plafond heures par jour",
        default=10.0,
        help="Pas de cumul au-delà de ce nombre d'heures par jour et par employé.",
    )
    presence_appliquer_defalcation = fields.Boolean(
        "Appliquer défalcation si heures insuffisantes",
        default=False,
        help="Si activé, les employés concernés par la politique verront leur salaire défalqué si < heures cibles/semaine.",
    )
    # Alertes et sanctions (2 alertes, 3e = sanction)
    presence_nb_alertes_avant_sanction = fields.Integer(
        "Nombre d'alertes avant sanction",
        default=2,
        help="Après ce nombre d'alertes (retard / absence non justifiée), la prochaine occurrence déclenche une sanction.",
    )
    presence_sanction_type = fields.Selection(
        [("fixe", "Montant fixe"), ("pourcentage", "Pourcentage du salaire")],
        string="Type de sanction",
        default="fixe",
    )
    presence_sanction_montant = fields.Float("Montant sanction (fixe)", digits="Account")
    presence_sanction_taux = fields.Float("Taux sanction (%)", digits=(5, 2))
