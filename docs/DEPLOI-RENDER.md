# Déployer COYA.PRO sur Render

## 1. Type de service : **Docker** (pas Python)

- Dans **New Web Service**, section **Environment** / **Language**, choisir **Docker** (pas Python 3).
- Render détectera le `Dockerfile` à la racine du repo.

## 2. Build / Start Command

- **Build Command** : laisser vide (Render build l’image Docker).
- **Start Command** : laisser vide (le `CMD` du Dockerfile démarre Odoo).

## 3. Variables d’environnement

Dans **Environment Variables**, ajouter (valeurs Supabase) :

| Clé         | Valeur / remarque |
|------------|---------------------|
| `DB_HOST`  | Host du pooler Session Supabase (ex. `aws-0-eu-north-1.pooler.supabase.com`) |
| `DB_USER`  | User Supabase (ex. `postgres.xxxx`) |
| `DB_PASSWORD` | Mot de passe Supabase |
| `DB_PORT`  | `5432` (pooler Session) |

`PORT` est fourni automatiquement par Render (port HTTP). Ne pas le définir pour la base.

## 4. Instance

- **Starter (512 MB)** : insuffisant pour Odoo.
- Utiliser au minimum **Standard** (2 GB RAM, 1 CPU) ou **Pro** (4 GB) pour une équipe &lt; 100.

## 5. Région

- Choisir une région proche des utilisateurs (ex. **Oregon (US West)** ou **Frankfurt** si dispo).

## 6. Déploiement

- Après sauvegarde, Render build l’image puis déploie. L’URL du service apparaît dans le dashboard (ex. `https://coya-senegel.onrender.com`).

## Référence

- [Docker on Render](https://render.com/docs/docker)
- Connexion Supabase : `docs/SUPABASE-IPV4.md`
