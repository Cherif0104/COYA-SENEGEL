{
    "name": "COYA Juridique",
    "summary": "Risques juridiques, contrats, conformité, contentieux — tableau de bord juridique",
    "version": "18.0.1.0.0",
    "author": "SENEGEL",
    "website": "https://coya.pro",
    "category": "COYA",
    "license": "LGPL-3",
    "depends": ["base", "coya_departments"],
    "data": [
        "security/ir.model.access.csv",
        "views/risque_views.xml",
        "views/contrat_views.xml",
        "views/contentieux_views.xml",
        "views/menu_views.xml",
    ],
    "installable": True,
    "application": False,
}
