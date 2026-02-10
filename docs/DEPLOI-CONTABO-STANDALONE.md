# Option B : Contabo sans Supabase (Odoo + Postgres sur le VPS)

## Ton plan Contabo (Cloud VPS 10) le permet-il ?

**Oui.** Cloud VPS 10 = 4 vCPU, 8 Go RAM, 75 Go NVMe (ou 150 Go SSD). C’est suffisant pour :
- **PostgreSQL** : ~1–2 Go RAM
- **Odoo** : ~2–4 Go RAM
- Le reste pour le système. Tu peux faire tourner Odoo + Postgres sur le même VPS sans problème.

---

## Lancer en production (sur le VPS)

```bash
cd /opt/COYA-SENEGEL
docker compose -f docker-compose.contabo.yml up -d
```

**Première fois** (base vide) : il faut initialiser la base Odoo (module `base`) :

```bash
docker compose -f docker-compose.contabo.yml run --rm odoo odoo -c /etc/odoo/odoo-standalone.conf -d postgres -i base --stop-after-init --without-demo=all
```

Puis redémarrer :

```bash
docker compose -f docker-compose.contabo.yml up -d
```

Accès : `http://IP_DU_VPS:8069`

---

## Sauvegardes et backups (sans code)

### 1. Auto Backup Contabo (recommandé, payant)

- Dans le panel Contabo : **Manage** sur ton VPS → **Order Add-On** (ou section Backup).
- Souscription à **Auto Backup** (~0,93 $/mois).
- Sauvegardes **automatiques** (ex. 10 derniers jours), **hors serveur**, restauration en **quelques clics** dans le panel.
- Aucun script à écrire : tout se gère depuis l’interface Contabo.

### 2. Snapshots (manuel, selon ton offre)

- Panel : **VPS control** → sur la ligne de ton VPS, bouton **Snap** (ou **Snapshot**).
- **Créer un snapshot** avant une grosse mise à jour ou une manip risquée.
- En cas de souci : **restaurer** ce snapshot depuis le panel.
- Les snapshots sont parfois limités à certains types de VPS (ex. High-Performance) ; à vérifier dans ton contrat.

### 3. Résumé

| Méthode        | Sans code ? | Coût      | Usage                    |
|----------------|-------------|-----------|---------------------------|
| **Auto Backup**| Oui (panel) | ~0,93 $/mois | Sauvegardes auto, restauration en 2 clics |
| **Snapshot**   | Oui (panel) | Inclus / selon offre | Point de restauration manuel avant changement |

Pour gérer sauvegardes et backups **sans toucher au code** : activer **Auto Backup** et utiliser les **Snapshots** depuis le panel Contabo.
