# Connexion du MCP Supabase dans Cursor

Le MCP Supabase est configuré dans `.cursor/mcp.json` pour le projet **COYA** (`ilpmgqguqkueioopqpma`).  
Si le bouton « Se connecter » n’ouvre pas le navigateur (OAuth), utilise l’**authentification par jeton (PAT)**.

## 1. Créer un jeton d’accès Supabase

1. Ouvre **https://supabase.com/dashboard/account/tokens**
2. Connecte-toi à ton compte Supabase (Google ou autre)
3. Clique sur **Generate new token**
4. Donne un nom (ex. `Cursor MCP COYA`)
5. Copie le token généré **tout de suite** (il ne sera plus affiché ensuite)

## 2. Donner le jeton à Cursor

La config MCP utilise la variable d’environnement `SUPABASE_ACCESS_TOKEN`. Cursor doit la voir au démarrage.

### Option A – Variable d’environnement utilisateur (Windows)

1. Ouvre **Paramètres Windows** → **Système** → **À propos** → **Paramètres système avancés**
2. **Variables d’environnement**
3. Sous **Variables utilisateur**, **Nouvelle** :
   - Nom : `SUPABASE_ACCESS_TOKEN`
   - Valeur : le token copié
4. **OK**, puis **ferme et rouvre Cursor** pour que la variable soit prise en compte.

### Option B – PowerShell (session en cours)

Dans un terminal PowerShell, avant de lancer Cursor :

```powershell
$env:SUPABASE_ACCESS_TOKEN = "ton_token_ici"
```

Puis lance Cursor **depuis ce même terminal** (ex. `cursor .`) pour que la variable soit disponible.

## 3. Vérifier la connexion

1. Redémarre Cursor (quitter complètement puis rouvrir)
2. Va dans **Paramètres** → **Cursor Settings** → **Tools & MCP**
3. Le serveur **supabase** doit apparaître comme connecté (sans demander « Se connecter »)
4. En chat, tu peux demander par ex. : « Liste les tables de la base avec le MCP Supabase »

## Sécurité

- Ne committe **jamais** le token dans le dépôt.
- Le token a les mêmes droits que ton compte Supabase ; garde-le secret.
- Pour limiter les risques, utilise de préférence un projet de dev, pas la prod.
