# Tester COYA.PRO en local avec la BDD sur le VPS

Tu peux lancer Odoo sur ta machine (Docker Desktop) en te connectant à la base PostgreSQL qui tourne sur le VPS. Utile pour débugger sans importer la BDD.

---

## 1. Autoriser l’accès PostgreSQL depuis ta machine (sur le VPS)

La base est dans le conteneur `db` sur le VPS. Il faut exposer le port 5432 et autoriser les connexions distantes.

### Option A : Exposer le port PostgreSQL du conteneur

Sur le VPS, dans `docker-compose.contabo.yml`, ajoute pour le service `db` :

```yaml
  db:
    image: postgres:16
    ports:
      - "5432:5432"   # ajouter cette ligne pour exposer PostgreSQL
    environment:
      ...
```

Puis redémarrer : `docker compose -f docker-compose.contabo.yml up -d`.

### Option B : Configurer PostgreSQL pour accepter les connexions réseau

Dans le conteneur `db` sur le VPS :

```bash
docker compose -f docker-compose.contabo.yml exec db bash
```

Éditer `/var/lib/postgresql/data/pg_hba.conf` (ou le fichier indiqué dans la config) et ajouter une ligne pour ton IP (remplace `TON_IP` par ton IP publique, ou `0.0.0.0/0` pour toute IP) :

```
host    all    all    TON_IP/32    md5
```

Puis dans `postgresql.conf` s’assurer que `listen_addresses = '*'`. Redémarrer le conteneur `db`.

### Pare-feu VPS

Ouvrir le port 5432 pour ton IP (ou temporairement pour 0.0.0.0) :

```bash
# ufw (exemple)
sudo ufw allow from TON_IP to any port 5432
sudo ufw reload
```

---

## 2. Lancer Odoo en local

Sur ta machine (avec Docker Desktop) :

```bash
cd C:\chemin\vers\SunuGest   # ou D:\DEVLAB & DEVOPS\SunuGest
docker compose -f docker-compose.local-vps-db.yml up -d
```

Ouvre **http://localhost:8069**. Tu utilises la même base que sur le VPS (donc les mêmes données).

Pour changer l’IP du VPS, édite `config/odoo-local-vps.conf` (champ `db_host`) et `docker-compose.local-vps-db.yml` (variable `HOST`).

---

## 3. Erreur `ERR_CONTENT_LENGTH_MISMATCH` (page blanche)

Cette erreur signifie qu’un fichier (souvent `web.assets_web.min.js`) est reçu tronqué : la taille reçue ne correspond pas à l’en-tête `Content-Length`. Causes fréquentes :

- **Cache navigateur** : fichier ancien ou corrompu en cache.
- **Réseau / proxy** : coupure ou proxy qui tronque la réponse.
- **Serveur / Docker** : processus Odoo ou nginx qui coupe la réponse.

### À faire côté navigateur

1. Vider le cache (Ctrl+Shift+Suppr → cocher “Images et fichiers en cache”) ou tester en **navigation privée**.
2. Recharger en forcé : **Ctrl+F5** (ou Cmd+Shift+R sur Mac).

### À faire côté VPS (si l’erreur est sur 5.189.175.90:8069)

1. Redémarrer Odoo pour régénérer les assets :
   ```bash
   docker compose -f docker-compose.contabo.yml restart odoo
   ```
2. Si tu passes par un reverse proxy (nginx, Traefik, etc.), augmenter les buffers et timeouts pour les grosses réponses (assets).
3. Tester en local avec la même BDD (`docker-compose.local-vps-db.yml`) : si l’erreur disparaît en local, le problème vient du réseau ou du serveur devant le VPS.

### Tester en local

En lançant Odoo en local avec la BDD VPS, tu contournes le chemin réseau jusqu’au VPS pour les assets (tout part de ta machine). Si la page s’affiche correctement en local, cela confirme un souci de livraison des assets depuis le VPS (réseau, proxy, ou Docker sur le VPS).
