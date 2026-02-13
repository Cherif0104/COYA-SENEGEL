# COYA Modern Navbar & Dashboard

Module dédié pour la navbar moderne fixe à gauche (dépliable au survol) et l'écran d'accueil avec toutes les applications accessibles.

## Fonctionnalités

- **Sidebar fixe gauche** : collapsed (70px, icônes seulement) / expanded au survol (260px, icônes + texte)
- **Fond vert SENEGEL** : charte graphique COYA respectée
- **Pas de menus déroulants** : navigation fixe, dépliable au survol uniquement
- **Écran d'accueil** : affiche toutes les applications auxquelles l'utilisateur a accès selon ses habilitations
- **Vue 360°** : dashboard avec toutes les fonctionnalités accessibles

## Installation

1. Activer le mode développeur dans Odoo
2. Mettre à jour la liste des applications
3. Rechercher "COYA Modern Navbar" → Installer

## Structure

- `views/coya_navbar_templates.xml` : Template qui remplace la navbar Odoo par la sidebar moderne
- `views/coya_home_dashboard_views.xml` : Action client et menu pour l'écran d'accueil
- `views/coya_home_dashboard_templates.xml` : Template QWeb pour le dashboard
- `static/src/scss/coya_navbar.scss` : Styles de la sidebar et du dashboard
- `static/src/js/coya_navbar.js` : JavaScript pour charger les apps et gérer les interactions

## Approche "1 module = 1 besoin"

Ce module suit l'approche définie dans `docs/MODULES-ONE-PER-NEED.md` : un module dédié pour cette fonctionnalité spécifique, indépendant du branding général.
