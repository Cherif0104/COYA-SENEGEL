# Déployer COYA.PRO sur OVH ou Contabo (VPS)

Hébergement sur un VPS avec Docker : même principe qu’en local (`docker-compose.supabase.yml` + `.env`).

---

## 1. Choisir l’hébergeur et la taille

### OVHcloud
- **Page VPS** : https://www.ovhcloud.com/en/vps/
- **Comparer les VPS** : https://www.ovhcloud.com/en/vps/compare/
- Pour une équipe &lt; 100 : **VPS Value** (ex. 4–8 Go RAM). Vérifier les offres actuelles (VPS-1, VPS-2, etc.).

### Contabo
- **Tarifs VPS** : https://contabo.com/en/pricing/
- **Cloud VPS** : https://contabo.com/en/vps/cloud-vps/
- Pour une équipe &lt; 100 : **Cloud VPS 10** (8 Go RAM, 4 vCPU, ~4,50 €/mois) ou **Cloud VPS 20** (12 Go RAM, ~7 €/mois).

---

## 2. Commander le VPS

- **OS** : **Ubuntu 22.04 LTS** (ou 24.04).
- Noter l’**IP publique**, le **login** (souvent `root`) et le **mot de passe** (ou clé SSH) fournis après création.

---

## 3. Se connecter en SSH

```bash
ssh root@TON_IP_VPS
```

(Remplace `TON_IP_VPS` par l’IP reçue.)

---

## 4. Installer Docker et Docker Compose

```bash
# Mise à jour
apt update && apt upgrade -y

# Docker
curl -fsSL https://get.docker.com | sh
usermod -aG docker root

# Docker Compose (plugin)
apt install -y docker-compose-plugin
```

Vérifier :

```bash
docker --version
docker compose version
```

---

## 5. Cloner le projet et configurer `.env`

```bash
cd /opt
git clone https://github.com/Cherif0104/COYA-SENEGEL.git
cd COYA-SENEGEL
```

Créer le fichier `.env` (mêmes variables que en local pour Supabase) :

```bash
nano .env
```

Contenu minimal (adapter avec tes vraies valeurs Supabase) :

```env
DB_HOST=aws-0-eu-north-1.pooler.supabase.com
DB_USER=postgres.XXXXXXXX
DB_PASSWORD=ton_mot_de_passe_supabase
DB_PORT=5432
```

Sauvegarder : `Ctrl+O`, `Entrée`, `Ctrl+X`.

---

## 6. Lancer COYA.PRO

```bash
cd /opt/COYA-SENEGEL
docker compose -f docker-compose.supabase.yml up -d
```

Vérifier que le conteneur tourne :

```bash
docker compose -f docker-compose.supabase.yml ps
```

Odoo écoute sur le port **8069** en interne. Pour l’exposer en HTTP :

- Soit ouvrir le port **8069** dans le firewall du VPS et accéder à `http://TON_IP_VPS:8069`.
- Soit installer un reverse proxy (Nginx ou Caddy) sur les ports 80/443 avec SSL (Let’s Encrypt) et faire proxy vers `localhost:8069`.

---

## 7. Firewall (à adapter selon ton besoin)

```bash
ufw allow 22
ufw allow 80
ufw allow 443
ufw allow 8069
ufw enable
```

---

## 8. (Optionnel) Nginx + SSL pour HTTPS

- Installer Nginx, configurer un virtual host qui proxy vers `127.0.0.1:8069`.
- Utiliser **Certbot** (Let’s Encrypt) pour un certificat gratuit sur ton nom de domaine pointant vers l’IP du VPS.

---

## Références

- Connexion Supabase (IPv4, pooler) : `docs/SUPABASE-IPV4.md`
- Compose utilisé : `docker-compose.supabase.yml` à la racine du repo
