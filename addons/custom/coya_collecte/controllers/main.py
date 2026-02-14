# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request


class CoyaCollecteController(http.Controller):
    @http.route("/coya/fiche/<int:fiche_type_id>", type="http", auth="public", website=False)
    def fiche_public_form(self, fiche_type_id, bootcamp_id=None, cohorte_id=None, **post):
        """Formulaire public : affiche le formulaire et traite la soumission.
        Paramètres optionnels : bootcamp_id, cohorte_id (pour lier la réponse)."""
        FicheType = request.env["coya.fiche.type"].sudo()
        fiche_type = FicheType.browse(fiche_type_id).exists()
        if not fiche_type or not fiche_type.active:
            return request.not_found()

        if request.httprequest.method == "POST":
            return self._process_submission(fiche_type, post, bootcamp_id, cohorte_id)

        return request.render(
            "coya_collecte.fiche_public_form_template",
            {"fiche_type": fiche_type, "bootcamp_id": bootcamp_id, "cohorte_id": cohorte_id},
        )

    def _process_submission(self, fiche_type, post, bootcamp_id=None, cohorte_id=None):
        """Crée la réponse à partir des données POST."""
        Reponse = request.env["coya.fiche.reponse"].sudo()
        Ligne = request.env["coya.fiche.reponse.ligne"].sudo()

        vals = {"fiche_type_id": fiche_type.id, "state": "received"}
        bid = bootcamp_id or post.get("bootcamp_id")
        cid = cohorte_id or post.get("cohorte_id")
        if bid and hasattr(Reponse, "bootcamp_id"):
            try:
                vals["bootcamp_id"] = int(bid)
            except (TypeError, ValueError):
                pass
        if cid and hasattr(Reponse, "cohorte_id"):
            try:
                vals["cohorte_id"] = int(cid)
            except (TypeError, ValueError):
                pass

        reponse = Reponse.create(vals)

        for champ in fiche_type.champ_ids.sorted("sequence"):
            raw = post.get(champ.technical_name)
            if champ.champ_type == "boolean":
                value = "Oui" if raw else "Non"
            else:
                value = (raw or "").strip()
            Ligne.create({
                "reponse_id": reponse.id,
                "champ_id": champ.id,
                "value_text": value or "",
            })

        return request.render(
            "coya_collecte.fiche_public_thanks_template",
            {"fiche_type": fiche_type},
        )
