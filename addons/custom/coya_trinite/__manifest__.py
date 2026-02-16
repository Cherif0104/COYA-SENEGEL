{
    "name": "COYA Trinité",
    "summary": "Plans de paie conventionnels et scores Trinité (Productivité, Profitabilité, Professionnalisme)",
    "version": "18.0.1.0.0",
    "author": "SENEGEL",
    "website": "https://coya.pro",
    "category": "Human Resources/Trinité",
    "license": "LGPL-3",
    "depends": ["hr", "coya_planning", "coya_time_tracking", "coya_departments"],
    "data": [
        "security/ir.model.access.csv",
        "data/cron_data.xml",
        "views/trinite_views.xml",
        "views/trinite_week_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "coya_trinite/static/src/xml/trinite_dashboard.xml",
            "coya_trinite/static/src/js/trinite_dashboard.js",
            "coya_trinite/static/src/scss/trinite_dashboard.scss",
        ],
    },
    "installable": True,
    "application": False,
}
