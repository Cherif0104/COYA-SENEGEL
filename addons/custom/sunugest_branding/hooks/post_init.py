# -*- coding: utf-8 -*-
# Part of COYA.PRO. See LICENSE file for full copyright and licensing details.

from odoo import api


def post_init_hook(cr, registry):
    """Renomme le partenaire OdooBot en « Assistant COYA » (debranding)."""
    env = api.Environment(cr, api.SUPERUSER_ID, {})
    partners = env["res.partner"].search([("name", "ilike", "OdooBot")])
    if partners:
        partners.write({"name": "Assistant COYA"})
