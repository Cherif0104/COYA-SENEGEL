#!/usr/bin/env bash
set -e

# Déploiement COYA.PRO sur VPS Contabo depuis GitHub Actions ou SSH
# - Met à jour le code
# - Met à jour les modules Odoo custom
# - Redémarre le conteneur Odoo

REPO_DIR="/opt/COYA-SENEGEL"
COMPOSE_FILE="docker-compose.contabo.yml"
DB_NAME="postgres"
MODULES="sunugest_branding,coya_modern_navbar"
ODOO_CONF="/etc/odoo/odoo-standalone.conf"

cd "$REPO_DIR"

echo "[deploy] Pull Git…"
git pull origin main

echo "[deploy] Update modules: $MODULES…"
docker compose -f "$COMPOSE_FILE" run --rm odoo odoo \
  -c "$ODOO_CONF" \
  -u "$MODULES" \
  -d "$DB_NAME" \
  --stop-after-init

echo "[deploy] Restart Odoo container…"
docker compose -f "$COMPOSE_FILE" restart odoo

echo "[deploy] Done."

