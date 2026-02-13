# Compatibilité Odoo 18 – COYA.PRO

Ce document concerne le module custom **sunugest_branding** (charte COYA.PRO / SENEGEL).

---

## Module actif

| Module | Rôle |
|--------|------|
| **sunugest_branding** | Identité COYA.PRO : titre, favicon, login, couleurs, overlay de chargement, page hors ligne |

---

## Modifications Odoo 18

- **Login** : formulaire et libellés COYA en français ; layout deux panneaux géré par le module (classe `coya-login-page`, SCSS dédié).
- **Assets** : SCSS dans `web.assets_common`, `web.assets_frontend`, `web.assets_backend` ; overlay splash en JS dans `web.assets_backend`.

---

## Checklist avant déploiement

- [ ] Aucune erreur de linter sur `addons/custom/sunugest_branding/`
- [ ] `git status` propre → commit + push

---

## Approche modules

Chaque besoin = un module dédié (ex. un futur module pour le style du menu des applications). Voir **docs/MODULES-ONE-PER-NEED.md**.
