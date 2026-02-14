{
    "name": "COYA Time Tracking",
    "summary": "Suivi du temps réel : pointage, saisie manuelle, types d'activité, lien avec projets",
    "version": "18.0.1.0.0",
    "author": "SENEGEL",
    "website": "https://coya.pro",
    "category": "Human Resources/Time Tracking",
    "license": "LGPL-3",
    "depends": ["hr", "hr_attendance", "coya_planning", "project"],
    "data": [
        "security/ir.model.access.csv",
        "views/time_entry_views.xml",
    ],
    "installable": True,
    "application": False,
}
