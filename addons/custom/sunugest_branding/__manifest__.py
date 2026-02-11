{
    "name": "COYA.PRO Branding",
    "summary": "Identité visuelle SENEGEL – COYA.PRO (charte CITOYENNETÉ, TRANSPARENCE, COMPÉTENCES)",
    "version": "18.0.1.1.0",
    "author": "SENEGEL",
    "website": "https://coya.pro",
    "category": "Web",
    "depends": ["web"],
    "data": [
        "views/sunugest_branding_templates.xml",
    ],
    "assets": {
        "web.assets_common": [
            "sunugest_branding/static/src/scss/sunugest_theme.scss",
        ],
        "web.assets_frontend": [
            "sunugest_branding/static/src/scss/sunugest_theme.scss",
        ],
        "web.assets_backend": [
            "sunugest_branding/static/src/scss/sunugest_theme.scss",
            "sunugest_branding/static/src/js/coya_splash_overlay.js",
        ],
    },
    "installable": True,
    "application": False,
}
