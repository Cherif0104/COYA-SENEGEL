# Connexion Odoo → Supabase en IPv4 — Instructions détaillées

Ce guide permet de connecter Odoo (dans Docker) à ta base Supabase lorsque ton réseau ou Docker **n’a pas d’IPv6**. Sans cela, tu obtiens l’erreur :  
`connection to server at "db.xxx.supabase.co" (2a05:...) port 6543 failed: Network is unreachable`.

La solution est d’utiliser le **pooler Supabase en mode Session**, qui accepte l’IPv4.

---

## Ce dont tu as besoin

- Un projet Supabase (ici : **COYA**, référence `ilpmgqguqkueioopqpma`).
- Le **mot de passe** de la base (celui défini dans Supabase pour l’utilisateur `postgres`).
- Le fichier **`.env`** à la racine du projet SunuGest (dossier `D:\DEVLAB & DEVOPS\SunuGest`).

---

## Étape 1 — Ouvrir le tableau de bord Supabase

1. Ouvre ton navigateur.
2. Va sur : **https://supabase.com/dashboard**
3. Connecte-toi si nécessaire.
4. Clique sur ton projet **COYA** (ou celui dont la référence est `ilpmgqguqkueioopqpma`).

Tu dois être sur la page d’accueil du projet (Overview).

---

## Étape 2 — Ouvrir la fenêtre « Connect »

1. En haut de la page, dans la barre du projet, repère le bouton **« Connect »** (souvent à droite).
2. Clique sur **« Connect »**.
3. Une fenêtre modale s’ouvre avec le titre **« Connect to your project »** et l’onglet **« Connection String »**.  
   Si tu vois l’avertissement **« Not IPv4 compatible »** et une URI avec **`db....supabase.co`**, tu es en **Direct connection** : passe à l’étape 3 pour changer le mode en **Session**.

---

## Étape 3 — Choisir le mode « Session » (et non Direct ou Transaction)

Tu es dans la fenêtre **« Connect to your project »**, onglet **« Connection String »**.

1. Repère le menu déroulant **« Method »** (souvent sous « Source » ou à côté de « Direct connection »).
2. S’il est sur **« Direct connection »** :
   - Tu peux voir l’avertissement **« Not IPv4 compatible »** et le texte : *« Use Session Pooler if on a IPv4 network »*.
   - L’URI affichée contient **`db.ilpmgqguqkueioopqpma.supabase.co`** → cette connexion ne fonctionnera pas en IPv4.
3. **À faire :** ouvre le menu **« Method »** et sélectionne **« Session »** (ou **« Session pooler »** / option qui parle de Session).  
   Ne garde **pas** « Direct connection » et n’utilise **pas** « Transaction » pour Odoo.

Résumé des modes :

- **Direct connection** — IPv6 uniquement → **ne pas utiliser** (message « Not IPv4 compatible »).
- **Session** (ou Session pooler) — Compatible IPv4 → **c’est celui-ci qu’il faut choisir.**
- **Transaction** — Autre mode pooler → ne pas utiliser pour Odoo ici.

---

## Étape 4 — Récupérer le Host, l’utilisateur et le port

Une fois le mode **Session** sélectionné, la page affiche une **chaîne de connexion** (URI) et/ou des champs séparés. Tu dois en extraire :

| Champ à noter | Exemple | Où le trouver |
|--------------|--------|----------------|
| **Host** | `aws-0-eu-west-1.pooler.supabase.com` | Dans l’URI : la partie entre `@` et `:5432` (ou le champ « Host » s’il est affiché). Le host doit contenir **`pooler.supabase.com`** et souvent **`aws-0-`** + une région. |
| **User** | `postgres.ilpmgqguqkueioopqpma` | Dans l’URI : la partie entre `postgres://` et `:`. Souvent de la forme **`postgres.[PROJECT_REF]`**. Pour ton projet : **`postgres.ilpmgqguqkueioopqpma`** (à confirmer selon ce qu’affiche le dashboard). |
| **Port** | `5432` | Pour le mode Session, le port affiché est en général **5432**. |
| **Password** | (ton mot de passe) | C’est le mot de passe de l’utilisateur `postgres` que tu as défini dans Supabase (Settings → Database). Si tu l’as oublié, tu peux le réinitialiser dans le dashboard. |

**Important :**

- Ne note **pas** un host du type **`db.ilpmgqguqkueioopqpma.supabase.co`** : c’est la connexion directe (IPv6 uniquement).
- Le host doit ressembler à : **`aws-0-XX-XX.pooler.supabase.com`** (avec une région à la place de `XX-XX`).

Note ces 4 valeurs sur un papier ou dans un fichier temporaire avant de passer à l’étape suivante.

---

## Étape 5 — Créer ou modifier le fichier `.env` à la racine du projet

1. Ouvre l’explorateur de fichiers et va dans le dossier du projet :  
   **`D:\DEVLAB & DEVOPS\SunuGest`**
2. À la **racine** de ce dossier (pas dans un sous-dossier), cherche le fichier **`.env`**.
   - S’il n’existe pas : crée un nouveau fichier texte et nomme-le exactement **`.env`** (sans extension .txt).
3. Ouvre le fichier **`.env`** avec un éditeur de texte (Bloc-notes, Notepad++, VS Code, etc.).

---

## Étape 6 — Remplir le `.env` avec les bonnes variables

Dans le fichier **`.env`**, écris ou remplace le contenu par les lignes suivantes en **remplaçant** les valeurs par celles que tu as notées à l’étape 4 :

```env
DB_HOST=aws-0-eu-west-1.pooler.supabase.com
DB_USER=postgres.ilpmgqguqkueioopqpma
DB_PASSWORD=ton_mot_de_passe_ici
```

**À adapter :**

- **`DB_HOST`** : remplace par le **Host** exact copié depuis le dashboard (mode Session), par ex. `aws-0-eu-west-1.pooler.supabase.com`. Pas d’espace avant ni après le `=`.
- **`DB_USER`** : remplace par l’**utilisateur** affiché (souvent `postgres.ilpmgqguqkueioopqpma`). Pas d’espace.
- **`DB_PASSWORD`** : remplace **`ton_mot_de_passe_ici`** par le vrai mot de passe de la base (celui de l’utilisateur postgres dans Supabase). Pas d’espace. Si le mot de passe contient des caractères spéciaux (`#`, `=`, `@`, etc.), tu peux le mettre entre guillemets : `DB_PASSWORD="mon#mot@de=passe"`.

**Exemple de `.env` rempli :**

```env
DB_HOST=aws-0-eu-west-1.pooler.supabase.com
DB_USER=postgres.ilpmgqguqkueioopqpma
DB_PASSWORD=MonMotDePasse123
```

4. **Enregistre** le fichier `.env` et ferme l’éditeur.

---

## Étape 7 — Ouvrir PowerShell dans le dossier du projet

1. Ouvre **PowerShell** (clic droit sur Démarrer → Windows PowerShell, ou recherche « PowerShell »).
2. Tape la commande suivante puis appuie sur **Entrée** pour aller dans le dossier du projet :

```powershell
cd "D:\DEVLAB & DEVOPS\SunuGest"
```

Tu dois voir le chemin s’afficher dans l’invite : `PS D:\DEVLAB & DEVOPS\SunuGest>`

---

## Étape 8 — Arrêter les conteneurs existants

Tape la commande suivante puis **Entrée** :

```powershell
docker compose -f docker-compose.supabase.yml down
```

Résultat attendu : message du type « Container sunugest-odoo-1 Removed » et « Network sunugest_default Removed ». S’il n’y avait pas de conteneur lancé, le message peut être différent ; ce n’est pas grave.

---

## Étape 9 — Démarrer Odoo avec le nouveau `.env`

Tape la commande suivante puis **Entrée** :

```powershell
docker compose -f docker-compose.supabase.yml up -d
```

Résultat attendu : « Container sunugest-odoo-1 Created » (ou « Started ») et pas d’erreur rouge.

---

## Étape 10 — Vérifier que le conteneur tourne et se connecte à la base

1. Attends **environ 30 à 60 secondes**.
2. Vérifie que le conteneur est bien en cours d’exécution :

```powershell
docker ps -a --filter name=sunugest
```

Tu dois voir une ligne avec **STATUS** contenant **「 Up X seconds 」** (ou « Up X minutes ») et **PORTS** avec **8070->8069**. Si **STATUS** est « Exited », le conteneur s’est arrêté.

3. Affiche les logs du conteneur :

```powershell
docker logs sunugest-odoo-1 2>&1
```

- **Succès :** tu ne vois **plus** le message « Network is unreachable » ni l’adresse IPv6 `2a05:...`. Tu peux voir des lignes de démarrage Odoo ou des requêtes.
- **Échec :** tu vois encore « Database connection failure » et « Network is unreachable » → reprendre les étapes 3 à 6 (vérifier que tu as bien choisi le mode **Session** et le host **pooler.supabase.com** dans le `.env`).

---

## Étape 11 — Ouvrir Odoo dans le navigateur

1. Ouvre ton navigateur.
2. Va à l’adresse : **http://localhost:8070** ou **http://localhost:8070/web/login** pour afficher directement le formulaire de connexion (email / mot de passe).
3. Si une page « Database selector » s’affiche, une seule base (**postgres**) est proposée : clique dessus pour accéder au login. Ne pas utiliser l’URL `/web/database/selector` si elle affiche « The database manager has been disabled ».
4. Tu dois voir la **page de connexion Odoo** (écran de login). **Ne pas utiliser « Create database »** : la base **postgres** sur Supabase est déjà initialisée. Choisis la base **postgres** dans la liste (ou ouvre **http://localhost:8070/web/login?db=postgres**) et connecte-toi. Au premier accès, configure le compte administrateur avec l’adresse **techsupport@senegel.org** (super administrateur SENEGEL).
5. **Thème SENEGEL (logo en cercle, slogan)** : pour afficher le logo SENEGEL dans un cercle et le slogan « Create an opportunity youth of africa » sur la page de login, installe l’application **COYA.PRO Branding** : menu **Apps** → recherche « Branding » ou « COYA » → **Install** sur le module « COYA.PRO Branding ».

---

## Récapitulatif des commandes (copier-coller)

À exécuter dans PowerShell, dans le dossier `D:\DEVLAB & DEVOPS\SunuGest` :

```powershell
cd "D:\DEVLAB & DEVOPS\SunuGest"
docker compose -f docker-compose.supabase.yml down
docker compose -f docker-compose.supabase.yml up -d
```

Attendre 30 à 60 secondes, puis :

```powershell
docker ps -a --filter name=sunugest
docker logs sunugest-odoo-1 2>&1
```

Puis ouvrir dans le navigateur : **http://localhost:8070**

---

## Accès super administrateur (SENEGEL)

- **Email du super administrateur :** **techsupport@senegel.org**
- À utiliser comme identifiant de connexion (login) pour le compte administrateur de la base **postgres**. Au premier accès sur la base, crée ou configure l’utilisateur admin avec cette adresse. Une fois connecté, tu peux modifier le mot de passe et les infos dans **Paramètres → Utilisateurs et sociétés → Utilisateurs**.

---

## Dépannage

| Problème | À vérifier |
|----------|------------|
| « Network is unreachable » encore affiché | Tu utilises encore le host **`db.ilpmgqguqkueioopqpma.supabase.co`** dans le `.env`. Il faut utiliser le host du mode **Session** (contenant **`pooler.supabase.com`**). |
| « Password authentication failed » | Le mot de passe dans **`DB_PASSWORD`** dans le `.env` n’est pas le bon. Vérifie ou réinitialise le mot de passe dans Supabase (Settings → Database). |
| Conteneur « Exited » après quelques secondes | Regarde les logs avec `docker logs sunugest-odoo-1 2>&1`. Si c’est une erreur de connexion, revoir le Host / User / Password et le mode **Session**. |
| Le fichier `.env` ne semble pas lu | Vérifie que le fichier s’appelle bien **`.env`** (avec le point au début), qu’il est à la **racine** de `SunuGest`, et qu’il n’y a pas d’espace autour du `=` (ex. `DB_HOST=aws-0-...`). |

---

## Résumé des valeurs à ne pas confondre

| À utiliser (mode Session, IPv4) | À ne pas utiliser (direct, IPv6) |
|---------------------------------|-----------------------------------|
| Host : `aws-0-XX.pooler.supabase.com` | Host : `db.ilpmgqguqkueioopqpma.supabase.co` |
| Port : `5432` | Port : `5432` ou `6543` sur l’host direct |
| User : `postgres.ilpmgqguqkueioopqpma` | User : `postgres` seul (sans le .ilpmgqguqkueioopqpma) |

Une fois le **Host** du mode Session et le **User** corrects dans le `.env`, la connexion Odoo → Supabase doit fonctionner en IPv4.

---

## Première utilisation : initialiser la base (erreur 500 « Internal Server Error »)

Si le conteneur tourne mais que **http://localhost:8070** affiche « Internal Server Error » ou « relation ir_module_module does not exist », la base **postgres** sur Supabase n’a pas encore été initialisée par Odoo. Il faut lancer **une seule fois** l’installation du module de base.

Si l’init échoue avec **« canceling statement due to lock timeout »**, c’est que le pooler Supabase coupe les requêtes trop longues ou qu’un autre processus (le serveur Odoo) tient des verrous. Suivre toute la procédure ci‑dessous.

---

### A. Augmenter les timeouts dans Supabase (recommandé)

1. Ouvre le **Supabase Dashboard** → ton projet → **SQL Editor**.
2. Exécute la requête suivante (elle augmente les timeouts pour le rôle `postgres` le temps de l’init) :

```sql
ALTER ROLE postgres SET statement_timeout = '30min';
ALTER ROLE postgres SET lock_timeout = '30min';
```

3. Tu peux vérifier avec : `SHOW statement_timeout;` et `SHOW lock_timeout;` (dans une nouvelle requête).

---

### B. Réinitialiser la base si une précédente init a échoué (tables partielles)

Si une première init a planté en cours de route, des tables peuvent déjà exister et la réessayer peut lever « relation … already exists ». Dans ce cas, **uniquement si la base ne contient rien d’important**, tu peux réinitialiser le schéma `public` :

Dans **SQL Editor** Supabase :

```sql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
```

Ensuite, reprendre à l’étape C.

---

### C. Arrêter Odoo puis lancer l’init (une seule connexion)

1. Dans PowerShell, dossier du projet :

```powershell
cd "D:\DEVLAB & DEVOPS\SunuGest"
docker compose -f docker-compose.supabase.yml stop odoo
```

2. Lancer l’init dans un **conteneur à part** (pas le serveur Odoo) pour éviter les conflits de verrous. Le `.env` est utilisé automatiquement :

```powershell
docker compose -f docker-compose.supabase.yml run --rm odoo odoo -c /etc/odoo/odoo-supabase.conf -d postgres -i base --stop-after-init --without-demo=all
```

3. Attendre la fin (plusieurs minutes). Si tu as une erreur **« could not translate host name … to address »**, le conteneur créé par `run` n’a pas résolu le DNS. Dans ce cas, redémarre Odoo puis utilise la méthode avec `docker exec` (étape D).

4. Quand la commande est terminée (retour au prompt) :

```powershell
docker compose -f docker-compose.supabase.yml up -d
```

5. Ouvrir **http://localhost:8070** : page de login Odoo (création du compte admin au premier accès).

---

### D. Alternative : init avec `docker exec` (si `run` échoue au DNS)

À utiliser **seulement si** l’étape C échoue à cause du DNS (résolution du hostname du pooler).

1. Odoo doit être **démarré** : `docker compose -f docker-compose.supabase.yml up -d`
2. Remplacer `TON_MOT_DE_PASSE` par ton mot de passe DB, puis exécuter :

```powershell
docker exec sunugest-odoo-1 odoo -c /etc/odoo/odoo-supabase.conf --db_host=aws-1-eu-north-1.pooler.supabase.com --db_user=postgres.ilpmgqguqkueioopqpma --db_password="TON_MOT_DE_PASSE" -d postgres -i base --stop-after-init --without-demo=all
```

3. Attendre la fin, puis redémarrer : `docker compose -f docker-compose.supabase.yml restart odoo`
4. Ouvrir **http://localhost:8070**

Avec la méthode D, le serveur Odoo et l’init tournent en même temps ; avoir augmenté les timeouts (étape A) limite le risque de « lock timeout ».
