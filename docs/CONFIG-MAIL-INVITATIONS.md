# Configuration du serveur de messagerie – Invitations Odoo

Objectif : **envoyer les invitations (nouvel utilisateur / nouvel employé) directement depuis Odoo**, avec une adresse d’envoi soit **SENEGEL** (@senegel.org, Google for non-profit), soit **COYA** (@coya.pro, domaine acheté chez Netlify + Google Workspace).

Tu as accès à la **console Google (Admin)** pour les deux. Voici les étapes pour chaque option.

---

## 1. Choisir l’adresse d’envoi

| Option | Domaine | Usage typique |
|--------|--------|----------------|
| **SENEGEL** | @senegel.org | Google for non-profit déjà en place ; envoi depuis ex. `techsupport@senegel.org` ou `noreply@senegel.org`. |
| **COYA** | @coya.pro | Domaine géré dans Netlify DNS ; tu configures Google Workspace pour coya.pro ; envoi depuis ex. `noreply@coya.pro` ou `admin@coya.pro`. |

Une fois le choix fait, toute la config (DNS + Google + Odoo) se fait **pour ce domaine**.

---

## 2. Option A – Envoi avec SENEGEL (@senegel.org)

### 2.1 Vérifier Google Workspace (non-profit)

- **Admin Google** : https://admin.google.com  
- Vérifier que le domaine **senegel.org** est bien géré et que la messagerie fonctionne.
- Si besoin, créer une adresse dédiée aux envois Odoo, ex. :  
  `noreply@senegel.org` ou `techsupport@senegel.org`.

### 2.2 DNS (si tu gères senegel.org ailleurs)

Si le domaine senegel.org est déjà utilisé avec Google Workspace, les **MX, SPF, DKIM** sont en principe déjà bons. Sinon, chez le gestionnaire DNS du domaine, ajouter les enregistrements indiqués par Google (voir option B pour le principe).

### 2.3 Odoo – Serveur sortant (SMTP)

- Dans Odoo : **Paramètres** → **Technique** → **Serveurs de messagerie sortants**.
- **Créer** un serveur :
  - **Serveur SMTP** : `smtp.gmail.com`
  - **Port** : `587` (TLS recommandé)
  - **Connexion** : TLS
  - **Utilisateur** : l’adresse complète (ex. `techsupport@senegel.org`)
  - **Mot de passe** : **Mot de passe d’application** Google (pas le mot de passe du compte)  
    → Créer dans : Compte Google → Sécurité → Connexion à des applications → Mot de passe d’application.
  - **Adresse « De »** : la même adresse (ex. `techsupport@senegel.org`).
- Enregistrer et **tester l’envoi**. Si tout est vert, les invitations partiront avec cette adresse.

---

## 3. Option B – Envoi avec COYA (@coya.pro)

Le domaine **coya.pro** est géré dans **Netlify DNS** (tu as déjà A + CNAME pour le site). Il faut ajouter les enregistrements **mail** pour Google Workspace.

### 3.1 Google Workspace pour coya.pro

- Dans **Admin Google** : ajouter le domaine **coya.pro** (si pas déjà fait).
- Suivre l’assistant « Vérifier le domaine » ; Google te donnera une **valeur TXT** à mettre dans le DNS. Tu la mettras dans Netlify (voir ci‑dessous).
- Une fois le domaine vérifié, dans **Applications** → **Google Workspace** → **Gmail** → **Authentifier le courrier** :
  - **SPF** : Google indique d’ajouter un enregistrement TXT (voir 3.2).
  - **DKIM** : activer DKIM pour coya.pro ; Google fournit un nom d’enregistrement (ex. `google._domainkey`) et une valeur TXT longue à copier.

### 3.2 Enregistrements DNS dans Netlify

Dans **Netlify** → **Domain management** → **DNS** (ou **DNS records** pour coya.pro) :

1. **Vérification du domaine (Google)**  
   - Type : **TXT**  
   - Name : `@` ou `coya.pro` (selon ce que demande Google)  
   - Value : la chaîne fournie par l’assistant Google (ex. `google-site-verification=...`).  
   - TTL : 3600 (ou défaut).

2. **MX (réception du courrier)**  
   Ajouter **tous** les enregistrements MX fournis par Google. Exemple type :

   | Type | Name   | Value                   | Priority | TTL  |
   |------|--------|-------------------------|----------|------|
   | MX   | @      | ASPMX.L.GOOGLE.COM.     | 1        | 3600 |
   | MX   | @      | ALT1.ASPMX.L.GOOGLE.COM.| 5        | 3600 |
   | MX   | @      | ALT2.ASPMX.L.GOOGLE.COM.| 5        | 3600 |
   | MX   | @      | ALT3.ASPMX.L.GOOGLE.COM.| 10       | 3600 |
   | MX   | @      | ALT4.ASPMX.L.GOOGLE.COM.| 10       | 3600 |

   (Les valeurs exactes et priorités sont dans **Admin Google** → Domaine → Enregistrements MX.)

3. **SPF (envoi autorisé)**  
   - Type : **TXT**  
   - Name : `@` (ou `coya.pro`)  
   - Value : `v=spf1 include:_spf.google.com ~all`  
   - TTL : 3600.

4. **DKIM (signature des e-mails)**  
   - Type : **TXT**  
   - Name : celui donné par Google (ex. `google._domainkey`)  
   - Value : la longue chaîne fournie par Google (une seule ligne, sans retours à la ligne).  
   - TTL : 3600.

5. **(Optionnel) DMARC**  
   - Type : **TXT**  
   - Name : `_dmarc`  
   - Value : `v=DMARC1; p=none; rua=mailto:admin@coya.pro`  
   (À durcir plus tard, ex. `p=quarantine` ou `p=reject`, quand tout est stable.)

Ne pas supprimer les enregistrements **A** et **CNAME** existants (site coya.pro / Vercel). Attendre la propagation DNS (jusqu’à 24–48 h).

### 3.3 Créer l’adresse d’envoi dans Google

- Dans **Admin Google** → **Utilisateurs** : créer un utilisateur (ex. `noreply@coya.pro` ou `admin@coya.pro`) pour les envois Odoo.
- Optionnel : activer « Mot de passe d’application » pour ce compte (recommandé si 2FA activée).

### 3.4 Odoo – Serveur sortant (SMTP) pour COYA

- **Paramètres** → **Technique** → **Serveurs de messagerie sortants** → **Créer** :
  - **Serveur SMTP** : `smtp.gmail.com`
  - **Port** : `587`
  - **Connexion** : TLS
  - **Utilisateur** : ex. `noreply@coya.pro` (ou l’adresse créée)
  - **Mot de passe** : mot de passe d’application Google de ce compte
  - **Adresse « De »** : ex. `noreply@coya.pro` ou `COYA.PRO <noreply@coya.pro>`
- Tester l’envoi ; une fois réussi, ce serveur peut être défini par défaut pour les invitations.

---

## 4. Nom d’expéditeur affiché (éviter « Administrator »)

Par défaut, Odoo affiche le **nom de l’utilisateur** qui envoie l’email. Si l’admin s’appelle « Administrator », les invitations arrivent avec **« Administrator &lt;techsupport@senegel.org&gt; »**. Pour afficher **COYA.PRO** ou **SENEGEL** : **Paramètres** → **Utilisateurs & Sociétés** → **Utilisateurs** → ouvrir l’utilisateur **Administrator** → dans **Nom** mettre **COYA.PRO** ou **SENEGEL ONG** → Enregistrer. Les prochains emails afficheront ce nom.

**Débranding des e-mails** : le module **COYA.PRO Branding** remplace déjà dans les e-mails le pied de page « Powered by Odoo » par **COYA.PRO · SENEGEL** et la couleur mauve par le vert de la charte. Pense à **mettre à jour le module** après un `git pull` pour que les templates email soient rechargés.

## 5. Envoi des invitations depuis Odoo

- **Nouvel utilisateur** : **Paramètres** → **Utilisateurs** → **Créer** → cocher **Envoyer un email d’invitation par courrier électronique** (ou équivalent selon la version).
- **Nouvel employé** (module Employés) : à la création, si l’option d’envoi d’invitation existe, l’e-mail partira avec le serveur sortant configuré.
- L’expéditeur affiché sera celui configuré dans le serveur SMTP (SENEGEL ou COYA selon ton choix).

---

## 6. Résumé rapide

| Étape | SENEGEL (@senegel.org) | COYA (@coya.pro) |
|-------|------------------------|-------------------|
| Domaine / DNS | Déjà sur Google non-profit ; vérifier MX/SPF/DKIM si besoin. | Netlify DNS : MX + SPF + DKIM (+ vérification domaine Google). |
| Admin Google | Utiliser un compte existant ou créer noreply@senegel.org. | Ajouter domaine coya.pro, créer ex. noreply@coya.pro. |
| Odoo SMTP | smtp.gmail.com, 587, TLS, techsupport@senegel.org (ou noreply) + mot de passe d’application. | smtp.gmail.com, 587, TLS, noreply@coya.pro + mot de passe d’application. |
| Invitations | Paramètres → Utilisateurs / Employés → créer utilisateur → envoyer invitation. | Idem. |

Si tu indiques si tu pars sur **SENEGEL** ou **COYA** en premier, on peut détailler uniquement cette option (DNS exact Netlify, copies d’écran Admin Google, etc.).

---

## 7. (Optionnel) SMTP par fichier de config Odoo

Si tu préfères définir le serveur sortant dans le fichier de config (ex. sur Contabo) au lieu de l’interface Odoo, ajoute dans `odoo-standalone.conf` (ou le fichier chargé par le conteneur) :

```ini
[options]
# ... (reste de la config)

# SMTP pour envoi des mails (invitations, etc.)
email_from = noreply@coya.pro
smtp_server = smtp.gmail.com
smtp_port = 587
smtp_ssl = False
smtp_user = noreply@coya.pro
smtp_password = ton_mot_de_passe_application_google
```

- Remplacer par `techsupport@senegel.org` / le compte SENEGEL si tu choisis l’option SENEGEL.
- Le mot de passe doit être un **mot de passe d’application** Google (Sécurité → Mots de passe des applications), pas le mot de passe du compte.
- Redémarrer Odoo après modification du fichier.
