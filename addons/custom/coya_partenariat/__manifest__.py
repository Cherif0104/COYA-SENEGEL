{
    "name": "COYA Prospection & Partenariat",
    "summary": "Carte des partenaires, opportunités, pipeline, type/secteur/engagement, alertes",
    "version": "18.0.1.0.0",
    "author": "SENEGEL",
    "website": "https://coya.pro",
    "category": "COYA",
    "license": "LGPL-3",
    "depends": ["base", "coya_departments"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_views.xml",
        "views/opportunite_views.xml",
        "views/menu_views.xml",
    ],
    "installable": True,
    "application": False,
}
