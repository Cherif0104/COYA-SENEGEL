# Un module = un besoin

À partir de maintenant, chaque fonctionnalité ou personnalisation est portée par **un module dédié**. Cela permet de :

- Garder le code clair et maintenable
- Activer/désactiver une fonctionnalité sans toucher au reste
- Réutiliser des modules d’un projet à l’autre

---

## Modules actuels

| Module | Rôle |
|--------|------|
| **sunugest_branding** | Charte graphique COYA.PRO : couleurs, logo, login, overlay, footer, page hors ligne |
| **coya_modern_navbar** | Navbar fixe gauche dépliable au survol + écran d'accueil avec toutes les applications accessibles |

Tout ce qui est **identité visuelle globale** (login, header, couleurs, splash) reste dans **sunugest_branding**.

Le **menu de navigation et l'écran d'accueil** sont gérés par **coya_modern_navbar**.

---

## Exemples de futurs modules

- **Style du menu des applications** : personnalisation du sélecteur d’apps (barre, icônes, couleurs) → un module dédié, ex. `coya_menu_apps_style`.
- **Localisation Sénégal** : XOF, TVA, formes juridiques → à recréer en module dédié si le besoin revient.
- **Dashboard / KPIs** : un module par type de dashboard si besoin plus tard.

Pour chaque nouveau besoin : créer un nouveau répertoire sous `addons/custom/`, avec son `__manifest__.py`, et ne charger que les vues/assets nécessaires à ce besoin.
