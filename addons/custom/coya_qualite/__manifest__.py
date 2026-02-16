{
    "name": "COYA Qualité & Suivi performance",
    "summary": "Score qualité global — agrégation Trinité + audits + contrôles par département / personne",
    "version": "18.0.1.0.0",
    "author": "SENEGEL",
    "website": "https://coya.pro",
    "category": "COYA",
    "license": "LGPL-3",
    "depends": ["base", "coya_departments", "coya_trinite", "hr"],
    "data": [
        "security/ir.model.access.csv",
        "views/qualite_score_views.xml",
    ],
    "installable": True,
    "application": False,
}
