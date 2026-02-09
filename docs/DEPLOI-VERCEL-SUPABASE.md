# Déploiement COYA.PRO – Supabase (PostgreSQL) et hébergement Odoo

Ce guide décrit comment connecter **Odoo COYA.PRO** au projet **Supabase COYA** (PostgreSQL) et déployer l’application. L’entrée utilisateur est **directement la page de login** (plus de landing en `/`).

---

## 1. Supabase : base PostgreSQL pour Odoo

Odoo a besoin d’une base **PostgreSQL**. Le projet **COYA** sur Supabase sert de base pour Odoo.

### Récupérer les identifiants (projet COYA)

1. Ouvrir le tableau de bord [Supabase](https://supabase.com) et le projet **COYA**.
2. **Project Settings** → **Database** :
   - **Host** (ex. `db.xxxx.supabase.co`)
   - **Port** : `5432`
   - **Database** : `postgres`
   - **User** : `postgres`
   - **Password** : mot de passe de l’utilisateur (à garder secret)

3. **Connection string (URI)** :
   ```text
   postgresql://postgres:[MOT_DE_PASSE]@db.xxxx.supabase.co:5432/postgres
   ```

4. Pour Docker / Odoo, utiliser l’URL **directe** (port 5432), pas le « Session pooler ».

### Utiliser Supabase avec Odoo (Docker)

Le dépôt fournit un compose **sans service `db` local**, qui pointe vers Supabase :

1. Copier `.env.example` en `.env`.
2. Renseigner dans `.env` :
   - `DB_HOST` = host Supabase (ex. `db.xxxx.supabase.co`)
   - `DB_USER` = `postgres`
   - `DB_PASSWORD` = mot de passe Supabase (ne jamais committer `.env`).

3. Lancer :
   ```bash
   docker compose -f docker-compose.supabase.yml up -d
   ```

4. Ouvrir l’URL Odoo (ex. `http://localhost:8070`) : vous arrivez sur le **login COYA.PRO** (logo SENEGEL, slogan). Créer une base si demandé (Odoo la crée dans PostgreSQL Supabase).

---

## 2. Hébergement Odoo en production

Choisir un hébergeur (Railway, Render, Fly.io, VPS, etc.) et déployer le conteneur Odoo avec la même logique :

- **Variables d’environnement** : définir `HOST`, `USER`, `PASSWORD` (ou `DB_HOST`, `DB_USER`, `DB_PASSWORD` selon l’entrypoint) pointant vers le projet Supabase COYA.
- **Volumes** : conserver `addons/custom` et `config` (ou les monter depuis le dépôt / stockage).
- **data_dir** : prévoir un volume pour `/var/lib/odoo` si besoin (sessions, fichiers).

Documenter dans la doc de l’hébergeur les variables à définir et l’utilisation de `docker-compose.supabase.yml` (sans service `db`).

---

## 3. Domaine

- Prévoir un sous-domaine pour Odoo (ex. **`app.coya.pro`**).
- Configurer DNS et, si besoin, redirection du domaine principal vers `app.coya.pro`.
- Exposer Odoo en **HTTPS** (reverse proxy : Nginx, Caddy, ou option de l’hébergeur).

---

## 4. Récapitulatif des URLs (exemple)

| Élément        | Local                | Production (exemple)     |
|----------------|----------------------|---------------------------|
| Odoo (login)   | `http://localhost:8070` | `https://app.coya.pro` |
| Base de données| Supabase COYA        | Supabase COYA             |

---

## 5. Bonnes pratiques

- **Secrets** : ne jamais committer le mot de passe Supabase. Utiliser uniquement les variables d’environnement ou un fichier `.env` (ignoré par Git).
- **HTTPS** : en production, toujours exposer Odoo derrière HTTPS.
- **Sauvegardes** : utiliser les sauvegardes Supabase ou des exports `pg_dump` pour la base Odoo.

---

## 6. Ancienne landing (optionnel)

Le dossier `landing/` à la racine peut être conservé pour un usage statique (ex. Vercel) ou supprimé. S’il est conservé, mettre à jour les liens dans `landing/index.html` vers l’URL Odoo de prod (ex. `https://app.coya.pro`) au lieu de localhost.
