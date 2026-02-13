# Déploiement simple – COYA.PRO sur Contabo

Odoo Community + nos modules custom, hébergé sur le VPS Contabo. Pas de déploiement automatique : tu mets à jour quand tu veux.

---

## Mettre à jour le VPS (après un git push depuis ta machine)

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
