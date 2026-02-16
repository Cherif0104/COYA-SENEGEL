{
    "name": "COYA Conseil (Gouvernance)",
    "summary": "Tableau de bord temps réel pour administrateurs — KPIs Trinité, projets, alertes",
    "version": "18.0.1.0.0",
    "author": "SENEGEL",
    "website": "https://coya.pro",
    "category": "COYA",
    "license": "LGPL-3",
    "depends": ["web", "base", "coya_departments"],
    "data": [
        "views/conseil_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "coya_conseil/static/src/xml/conseil_board.xml",
            "coya_conseil/static/src/js/conseil_board.js",
        ],
    },
    "installable": True,
    "application": False,
}
