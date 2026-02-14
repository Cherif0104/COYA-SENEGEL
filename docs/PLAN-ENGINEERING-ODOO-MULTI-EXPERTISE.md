# Plan d’engineering – Plateforme multi-expertise Odoo

**Projet : COYA.PRO – Plateforme Odoo multi-tenant Sénégal (SENEGEL)**  
**Version : 1.0**  
**Statut : Priorités & lancement**

---

## 1. Vision et objectifs

### 1.1 Contexte

- Plateforme **multi-tenant** basée sur **Odoo** (open source).
- **Super-administrateur** = propriétaire de la plateforme.
- Organisations hébergées : entreprises, GIE, ONG, collectivités, organismes publics.
- Souveraineté numérique et adaptation au contexte **sénégalais**.
- Évolution possible vers une offre **SaaS**.

### 1.2 Objectifs

- Réutiliser du code open source validé et éprouvé.
- Fournir une plateforme **tout-en-un** (compta, RH, projets, stocks, etc.).
- Multi-organisations avec isolation par tenant.
- **50+ modules fonctionnels** couvrant tous les secteurs d’activité.
- Personnalisation ultérieure sans compromettre le socle.

---

## 2. Stack technique

### 2.1 Composants principaux

| Composant       | Technologie                         | Rôle                 |
|-----------------|-------------------------------------|----------------------|
| Application     | Odoo (Community ou Enterprise)      | Cœur ERP             |
| Base de données | PostgreSQL                          | Persistance          |
| Runtime         | Python 3.10+                        | Backend Odoo         |
| Frontend        | OWL (Odoo Web Library)              | Interface utilisateur|
| Déploiement     | Docker / VM                         | Production           |

### 2.2 Environnement de développement

- Python 3.10+
- Node.js (pour les assets front)
- PostgreSQL 14+
- Git
- Docker & Docker Compose (recommandé)

### 2.3 Références officielles

- [Odoo GitHub](https://github.com/odoo/odoo)
- [Documentation Odoo](https://www.odoo.com/documentation/)
- [OCA (Odoo Community Association)](https://github.com/OCA)

---

## 3. Architecture cible

### 3.1 Multi-tenancy Odoo

- **Companies** : chaque organisation = une ou plusieurs « companies » Odoo.
- **Multi-company rules** : isolation des données par company.
- **Shared / non-shared** : produits, partenaires partagés ou non selon besoin.

### 3.2 Super-administrateur plateforme

- Rôle technique dédié au-dessus des companies.
- Droits : créer/supprimer companies, activer modules, gestion globale.
- Implémentation : groupe Odoo type `base.group_system` + règles métier spécifiques (module custom ou script).

### 3.3 Structure des modules

```
COYA.PRO/
├── odoo-18/                 # Source Odoo 18.0 (clone officiel)
├── addons/
│   ├── oca/                 # Modules OCA (optionnel)
│   └── custom/              # Modules personnalisés
│       ├── sunugest_branding/  # Branding COYA.PRO / SENEGEL
│       ├── coya_modern_navbar/  # Navbar moderne + dashboard accueil
│       └── platform_admin/  # Super-admin plateforme
├── config/
│   └── odoo.conf
├── docker-compose.yml
└── docs/
```

---

## 4. Priorités de développement (phases)

### Phase 0 – Fondations (priorité immédiate)

| Priorité | Tâche                         | Livrable                          |
|----------|-------------------------------|-----------------------------------|
| P0       | Cloner Odoo, configurer Docker| Environnement Odoo fonctionnel en local |
| P0       | Nouvelle base PostgreSQL      | BDD dédiée pour Odoo              |
| P0       | Premier démarrage Odoo        | Odoo accessible (create database) |
| P0       | Activer multi-company         | Plusieurs companies configurables |
| P0       | Définir le rôle super-admin   | Groupe / règles de sécurité       |

### Phase 1 – Noyau métier (semaines 1–4)

| Priorité | Module / domaine    | Fonctionnalités principales                   |
|----------|---------------------|-----------------------------------------------|
| P1       | Contacts / Tiers    | Partenaires (clients, fournisseurs, contacts) |
| P1       | Comptabilité        | Journal, écritures, rapports de base          |
| P1       | Ventes              | Devis, commandes, facturation client          |
| P1       | Achats              | Demandes, commandes fournisseur               |
| P1       | Inventaire / Stock  | Produits, mouvements, inventaire              |

### Phase 2 – RH et projets (semaines 5–8)

| Priorité | Module / domaine | Fonctionnalités principales          |
|----------|------------------|--------------------------------------|
| P2       | Employés / RH    | Fiches employés, départements        |
| P2       | Feuilles de temps| Timesheets, projets                  |
| P2       | Projets          | Projets, tâches, jalons              |
| P2       | Congés           | Demandes, validation, soldes         |

### Phase 3 – Fonctions avancées (semaines 9–12)

| Priorité | Module / domaine | Fonctionnalités principales         |
|----------|------------------|-------------------------------------|
| P3       | CRM              | Opportunités, pipeline              |
| P3       | Fabrication      | BOM, ordres de fabrication (si besoin) |
| P3       | Marketing        | Campagnes, leads (si besoin)        |
| P3       | Helpdesk         | Tickets (ou intégration Zammad)     |
| P3       | Budget           | Budgets, contrôle des dépenses      |

### Phase 4 – Localisation Sénégal (continu)

| Priorité | Domaine            | Contenu                                 |
|----------|--------------------|------------------------------------------|
| P4       | Devise             | XOF comme devise par défaut              |
| P4       | Fiscalité          | TVA et règles fiscales locales           |
| P4       | Formes juridiques  | SA, SARL, GIE, association, ONG…        |
| P4       | Secteurs           | Nomenclatures adaptées au Sénégal        |
| P4       | Langues            | FR par défaut, EN optionnel              |

---

## 5. Base de données

### 5.1 Stratégie

- **Une base PostgreSQL dédiée** à Odoo.
- Ne pas partager la base avec d’autres applications.
- Backups réguliers (quotidiens en production).

### 5.2 Configuration type

```ini
# odoo.conf (extrait)
db_host = localhost  # ou host Supabase/Postgres
db_port = 5432
db_name = postgres
db_user = odoo
db_password = ***
```

### 5.3 Supabase (optionnel)

- Créer un nouveau projet Supabase pour Odoo.
- Utiliser uniquement PostgreSQL (connexion directe).
- Odoo gère son auth en interne ; Supabase Auth n’est pas utilisé pour Odoo.

---

## 6. Déploiement

### 6.1 Docker (recommandé)

```yaml
# docker-compose.yml (schéma simplifié)
services:
  odoo:
    image: odoo:18
    depends_on:
      - db
    ports:
      - "8069:8069"
    volumes:
      - ./addons/custom:/mnt/extra-addons
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=odoo
      - POSTGRES_PASSWORD=odoo
    volumes:
      - odoo-db-data:/var/lib/postgresql/data

volumes:
  odoo-db-data:
```

### 6.2 Production

- Reverse proxy (Nginx / Traefik) + HTTPS.
- Backup automatique de la base.
- Monitoring (logs, santé de l’instance).

---

## 7. Modules Odoo à activer (par défaut)

### 7.1 Phase 1

- `base`, `web`
- `crm` (optionnel en phase 1)
- `sale`, `purchase`
- `account`, `account_accountant`
- `stock`, `product`
- `contacts`

### 7.2 Phase 2

- `hr`, `hr_contract`, `hr_holidays`
- `project`, `project_timesheet`
- `hr_timesheet`

### 7.3 Phase 3

- `crm`, `sale_crm`
- `mrp` (si fabrication)
- `helpdesk` (Odoo 17+)
- `budgets` (module OCA ou custom)

---

## 8. Modules custom (à développer)

### 8.1 `senegal_base`

- Devise XOF par défaut.
- Formes juridiques sénégalaises.
- Paramètres fiscaux de base.
- Traductions / libellés locaux si besoin.

### 8.2 `platform_admin`

- Rôle super-admin plateforme.
- Vue globale des companies (si nécessaire).
- Gestion centralisée des organisations (création, activation, limites).

---

## 9. Bonnes pratiques

- **Ne pas modifier le code source d’Odoo** : tout custom dans des addons.
- Hériter des modèles existants (ex. `res.partner`) pour ajouter des champs.
- Tester en local avant tout changement en prod.
- Utiliser des branches Git pour chaque fonctionnalité.
- Documenter les personnalisations dans `docs/`.

---

## 10. Prochaines étapes immédiates

1. ~~Créer le dossier du projet COYA.PRO.~~ ✓
2. ~~Cloner Odoo depuis GitHub (branche 18.0).~~ ✓ → `odoo-18/`
3. Préparer `docker-compose.yml` et `odoo.conf`.
4. Créer une nouvelle base PostgreSQL.
5. Lancer Odoo et créer la première base via l’interface.
6. Activer multi-company et configurer 2 companies de test.
7. ~~Créer le squelette du module `senegal_base`.~~ ✓ Supprimé du projet. Si besoin : recréer un module dédié (XOF, TVA, formes juridiques Sénégal).

---

*Plan d’engineering pour COYA.PRO (SENEGEL) – Odoo multi-expertise. Priorités : fondations puis noyau métier.*
