{
    "name": "COYA.PRO Branding",
    "summary": "Identité visuelle SENEGEL – COYA.PRO (charte CITOYENNETÉ, TRANSPARENCE, COMPÉTENCES)",
    "version": "18.0.1.1.0",
    "author": "SENEGEL",
    "website": "https://coya.pro",
    "category": "Web",
    "license": "LGPL-3",
    "depends": ["web", "mail"],
    "data": [
        "views/sunugest_branding_templates.xml",
        "views/mail_templates_debrand.xml",
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
    "post_init_hook": "sunugest_branding.hooks.post_init:post_init_hook",
    "installable": True,
    "application": False,
}
