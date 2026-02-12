# Déployer COYA.PRO sur un VPS (OVH ou Contabo)

Même principe sur les deux : tu prends un VPS Ubuntu, tu installes Docker, tu clones le repo et tu lances le compose avec Supabase.

---

## Comparatif rapide

| | **Contabo** | **OVHcloud** |
|---|-------------|--------------|
| **Offre adaptée** | Cloud VPS 10 | VPS Value (ex. VPS-1) |
| **Prix (ordre d’idée)** | ~4–5 €/mois (4 vCPU, 8 Go RAM) | ~4–6 €/mois (4 vCPU, 8 Go RAM) |
| **Paiement** | Carte, PayPal | Carte, SEPA |
| **Liens** | [contabo.com/en/vps](https://contabo.com/en/vps) | [ovhcloud.com/vps](https://www.ovhcloud.com/en/vps) |

Pour une équipe &lt; 100 personnes, **4 vCPU / 8 Go RAM** suffisent (équivalent Cloud VPS 10 ou VPS Value 8 Go).

---

## Étapes communes (après création du VPS)

### 1. Connexion SSH

Tu reçois une **IP**, un **utilisateur** (souvent `root` ou `ubuntu`) et un **mot de passe** (ou clé SSH).

```bash
ssh root@TON_IP
# ou
ssh ubuntu@TON_IP
```

### 2. Mettre à jour et installer Docker

```bash
apt update && apt upgrade -y
curl -fsSL https://get.docker.com | sh
```

### 3. Installer Docker Compose (si pas inclus)

```bash
apt install docker-compose-plugin -y
# ou
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### 4. Cloner le projet

```bash
cd /opt
git clone https://github.com/Cherif0104/COYA-SENEGEL.git
cd COYA-SENEGEL
```

### 5. Fichier `.env` (Supabase)

Crée le fichier `.env` à la racine du projet (remplace par tes vraies valeurs Supabase) :

```bash
nano .env
```

Contenu type (voir `docs/SUPABASE-IPV4.md` pour les valeurs exactes) :

```
DB_HOST=aws-0-eu-north-1.pooler.supabase.com
DB_USER=postgres.XXXXXXXX
DB_PASSWORD=ton_mot_de_passe_supabase
DB_PORT=5432
```

Sauvegarde : `Ctrl+O`, `Entrée`, `Ctrl+X`.

### 6. Lancer Odoo

```bash
docker compose -f docker-compose.supabase.yml up -d
```

### 7. Ouvrir les ports (firewall)

- **OVH** : souvent ouvert par défaut pour 22, 80, 443. Si besoin : `ufw allow 8069` puis `ufw enable`.
- **Contabo** : idem ; autoriser au moins **8069** (Odoo) et **80/443** si tu mets un reverse proxy plus tard.

```bash
ufw allow 22
ufw allow 8069
ufw allow 80
ufw allow 443
ufw enable
```

### 8. Accès à l’application

- **Direct** : `http://TON_IP:8069`
- **Avec domaine + HTTPS** : installer Nginx (ou Caddy) en reverse proxy et Let’s Encrypt (voir doc dédiée si besoin).

---

## Commandes utiles

```bash
# Voir les logs Odoo
docker compose -f docker-compose.supabase.yml logs -f odoo

# Redémarrer
docker compose -f docker-compose.supabase.yml restart odoo

# Arrêter
docker compose -f docker-compose.supabase.yml down
```

---

## Références

- Connexion Supabase (IPv4, pooler) : `docs/SUPABASE-IPV4.md`
- Contabo VPS : https://contabo.com/en/vps
- OVH VPS : https://www.ovhcloud.com/en/vps
