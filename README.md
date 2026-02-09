# COYA.PRO

Plateforme Odoo **COYA.PRO** – identité **SENEGEL** (CITOYENNETÉ, TRANSPARENCE, COMPÉTENCES).  
Entrée directe sur la **page de connexion** ; plus de landing en `/`.

## Structure

```
COYA.PRO/
├── odoo-18/              # Odoo 18.0 (clone officiel)
├── addons/custom/        # Modules personnalisés
│   └── sunugest_branding/  # Branding COYA.PRO / SENEGEL (logo, couleurs, login)
├── landing/              # (Optionnel) Landing statique HTML – liens vers app Odoo
├── config/                # odoo.conf
├── docs/                  # Documentation
└── README.md
```

## Prérequis

**Option recommandée : Docker Desktop**
- [Télécharger Docker Desktop pour Windows](https://www.docker.com/products/docker-desktop/)

**Alternative :** Python 3.10–3.12 + PostgreSQL 14+ + Node.js

## Lancer Odoo en local

### Avec base PostgreSQL locale (docker-compose)

1. Dans le dossier du projet :
   ```bash
   docker compose up -d
   ```
2. Ouvrir **http://localhost:8070** → vous arrivez sur le **login COYA.PRO** (logo SENEGEL).
3. Créer la première base si besoin (assistant Odoo).

Pour arrêter : `docker compose down`

### Avec Supabase (projet COYA)

1. Copier `.env.example` en `.env` et renseigner `DB_HOST`, `DB_USER`, `DB_PASSWORD` (Supabase).
2. Lancer :
   ```bash
   docker compose -f docker-compose.supabase.yml up -d
   ```
3. Ouvrir **http://localhost:8070** → login COYA.PRO.

Voir [docs/DEPLOI-VERCEL-SUPABASE.md](docs/DEPLOI-VERCEL-SUPABASE.md) pour le déploiement et le domaine (ex. `app.coya.pro`).

## Branding COYA.PRO / SENEGEL

Le module **COYA.PRO Branding** (`addons/custom/sunugest_branding`) applique la charte SENEGEL (vert / jaune, logo, slogan) au login et à l’interface Odoo.

- **Titre des pages** : COYA.PRO  
- **Login** : logo SENEGEL, texte « Connexion », slogan « CITOYENNETÉ, TRANSPARENCE, COMPÉTENCES », footer « © SENEGEL · COYA.PRO — made in Africa ».

### Installation du module

1. Démarrer Odoo (voir ci-dessus).
2. **Paramètres** → Activer le **mode développeur**.
3. **Apps** → Mettre à jour la liste des applications.
4. Rechercher **COYA.PRO** ou **SENEGEL** → **COYA.PRO Branding** → **Installer**.

Si le module n’apparaît pas : redémarrer les conteneurs (`docker compose down` puis `docker compose up -d`), puis mettre à jour la liste des apps.

## Documentation

- [docs/DEPLOI-VERCEL-SUPABASE.md](docs/DEPLOI-VERCEL-SUPABASE.md) – Connexion Supabase COYA, hébergement, domaine.
- [docs/PLAN-ENGINEERING-ODOO-MULTI-EXPERTISE.md](docs/PLAN-ENGINEERING-ODOO-MULTI-EXPERTISE.md) – Phases de développement et modules métier.

## Prochaines étapes

1. Configurer la base (locale ou Supabase).
2. Activer les applications métier (CRM, Ventes, Comptabilité, etc.) selon [docs/PLAN-ENGINEERING-ODOO-MULTI-EXPERTISE.md](docs/PLAN-ENGINEERING-ODOO-MULTI-EXPERTISE.md) (phases 1–3).
3. Localisation Sénégal : activer et finaliser le module **senegal_base** (`addons/custom/senegal_base/`) – XOF, TVA, formes juridiques sénégalaises.
4. Dashboards : utiliser les vues tableau de bord Odoo ; dashboards personnalisés ou prédictifs à prévoir en module custom ou outil BI si besoin.
