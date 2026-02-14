# Déploiement simple – COYA.PRO sur Contabo

Odoo Community + modules custom (**sunugest_branding**, **coya_modern_navbar**). Les anciens modules (senegal_base, coya_dashboard) ont été supprimés du projet.

---

## Workflow : tout reste à jour

1. **Sur ta machine** : tu modifies le code → `git push origin main`
2. **Sur le VPS** : tu lances le script → le code est récupéré, les modules mis à jour, Odoo redémarré

Aucun import manuel de module dans Odoo : tout passe par le dépôt Git et le script de déploiement.

---

## Mettre à jour le VPS (après un git push)

1. **Connecte-toi au VPS** (mot de passe ou clé, comme d’habitude) :
   ```bash
   ssh root@TON_IP_VPS
   ```

2. **Lance ces 3 commandes** (copier-coller en une fois) :
   ```bash
   cd /opt/COYA-SENEGEL
   git pull origin main
   docker compose -f docker-compose.contabo.yml run --rm odoo odoo -c /etc/odoo/odoo-standalone.conf -u sunugest_branding,coya_modern_navbar -d postgres --stop-after-init
   docker compose -f docker-compose.contabo.yml restart odoo
   ```

C’est tout. Odoo redémarre avec le nouveau code.

---

## Variante : utiliser le script

Si le script est déjà sur le VPS :
```bash
cd /opt/COYA-SENEGEL
./scripts/deploy_contabo.sh
```

---

## En cas de souci

Voir **DEPLOI-CONTABO-FIX.md** (timeout, page blanche, etc.).
