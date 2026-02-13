# Dépannage – Page blanche, ERR_CONTENT_LENGTH_MISMATCH, colonnes manquantes

## Problèmes traités

1. **Page blanche / ERR_CONTENT_LENGTH_MISMATCH** sur `web.assets_web.min.js`
2. **Thread timeout** : `virtual real time limit (174/120s) reached`

---

## 1. Augmenter le timeout des threads (limit_time_real)

La page blanche et `ERR_CONTENT_LENGTH_MISMATCH` viennent du fait que le serveur coupe le transfert des assets après 120 secondes (connexion Sénégal → VPS Europe parfois lente).

Le fichier `config/odoo-standalone.conf` contient déjà :

```ini
limit_time_real = 300
```

Si tu utilises un autre fichier de config, ajoute cette ligne dans `[options]`.

---

## 2. Procédure de mise à jour sur le VPS

À faire **après** chaque `git pull` qui modifie les addons custom :

```bash
cd /opt/COYA-SENEGEL

# 1. Récupérer le code
git pull origin main

# 2. Mise à jour du module branding
docker compose -f docker-compose.contabo.yml run --rm odoo odoo \
  -c /etc/odoo/odoo-standalone.conf \
  -u sunugest_branding \
  -d postgres \
  --stop-after-init

# 3. Redémarrer Odoo
docker compose -f docker-compose.contabo.yml restart odoo
```

---

## 3. Navigateur

Après une mise à jour :

- Vider le cache (Ctrl+Shift+Delete)
- Ou rechargement forcé : Ctrl+Shift+R

---

## 4. En cas de persistance (page blanche)

Si la page reste blanche malgré tout :

1. Vérifier que `limit_time_real = 300` est bien dans le fichier de config monté par Docker.
2. Augmenter encore : `limit_time_real = 600`
3. Redémarrer :  
   `docker compose -f docker-compose.contabo.yml restart odoo`
