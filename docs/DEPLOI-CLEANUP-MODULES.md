# Nettoyage base de données (modules supprimés du projet)

Les modules **senegal_base** et **coya_dashboard** ont été **supprimés** du dépôt. Si la base Odoo les a encore enregistrés (ancienne installation), tu peux voir :

```
ERROR postgres odoo.modules.loading: Some modules are not loaded... ['coya_dashboard', 'senegal_base']
```

Ce fichier explique comment les retirer proprement de la base pour supprimer ce message.

---

## Solution : désinstaller proprement depuis Odoo

### Option 1 : Via l'interface web (recommandé)

1. Connecte-toi à Odoo : `http://TON_IP_VPS:8069`
2. **Paramètres** → **Activer le mode développeur**
3. **Apps** → **Rechercher "senegal" ou "coya_dashboard"**
4. Si les modules apparaissent comme **installés** :
   - Clique sur le module → **Désinstaller**
   - Répète pour les deux modules

### Option 2 : Via la ligne de commande (si besoin)

Sur le VPS :

```bash
cd /opt/COYA-SENEGEL
docker compose -f docker-compose.contabo.yml run --rm odoo odoo \
  -c /etc/odoo/odoo-standalone.conf \
  -d postgres \
  --stop-after-init \
  -u base \
  --uninstall senegal_base,coya_dashboard
```

Puis redémarrer :
```bash
docker compose -f docker-compose.contabo.yml restart odoo
```

---

## Après le nettoyage

1. **Installer le nouveau module** `coya_modern_navbar` :
   - **Apps** → **Mettre à jour la liste des applications**
   - Rechercher "COYA Modern Navbar" → **Installer**

2. **Vérifier** :
   - La sidebar moderne doit apparaître à gauche
   - Plus d'erreurs dans les logs concernant `senegal_base` ou `coya_dashboard`

---

## Nettoyage direct en base (avancé)

Si les modules n'apparaissent plus dans Apps (ils ont été supprimés du code), tu peux retirer les entrées restantes dans PostgreSQL :

```bash
docker compose -f docker-compose.contabo.yml exec db psql -U odoo -d postgres -c "DELETE FROM ir_module_module WHERE name IN ('senegal_base', 'coya_dashboard');"
```

Puis redémarrer Odoo.
