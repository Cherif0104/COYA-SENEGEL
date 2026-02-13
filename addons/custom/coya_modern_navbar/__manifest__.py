{
    "name": "COYA Modern Navbar & Dashboard",
    "summary": "Navbar fixe gauche dépliable au survol + écran d'accueil avec toutes les applications accessibles et vue 360°",
    "version": "18.0.1.0.0",
    "author": "SENEGEL",
    "website": "https://coya.pro",
    "category": "Web",
    "license": "LGPL-3",
    "depends": ["web", "base"],
    "data": [
        "views/coya_home_dashboard_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "coya_modern_navbar/static/src/xml/coya_home_dashboard.xml",
            "coya_modern_navbar/static/src/scss/coya_navbar.scss",
            "coya_modern_navbar/static/src/js/coya_navbar.js",
        ],
    },
    "installable": True,
    "application": False,
}
