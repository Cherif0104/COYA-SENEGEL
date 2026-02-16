{
    "name": "COYA Collecte",
    "summary": "Formulaires publics modulables : fiches par type, lien partageable, réponses centralisées",
    "version": "18.0.1.0.0",
    "author": "SENEGEL",
    "website": "https://coya.pro",
    "category": "Marketing/Surveys",
    "license": "LGPL-3",
    "depends": ["base", "web", "coya_departments"],
    "data": [
        "security/ir.model.access.csv",
        "views/fiche_templates.xml",
        "views/fiche_views.xml",
    ],
    "installable": True,
    "application": False,
}
