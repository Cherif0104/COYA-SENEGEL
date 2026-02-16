#!/usr/bin/env bash
# Phase 2 : Premier déploiement sur le VPS (clone/pull, Odoo+Postgres, init base)
# À exécuter sur le VPS (Ubuntu) après : apt update, install Docker, docker-compose-plugin
# Usage: bash vps_phase2_first_deploy.sh [--init-base] [--set-admin]
#   --init-base : première fois, initialise la base avec le module base (obligatoire si base vide)
#   --set-admin : définit admin sur techsupport@senegel.com (optionnel)

set -e
REPO_URL="${REPO_URL:-https://github.com/Cherif0104/COYA-SENEGEL.git}"
REPO_DIR="${REPO_DIR:-/opt/COYA-SENEGEL}"
COMPOSE_FILE="docker-compose.contabo.yml"
ODOO_CONF="/etc/odoo/odoo-standalone.conf"
DB_NAME="postgres"

INIT_BASE=false
SET_ADMIN=false
for arg in "$@"; do
  case "$arg" in
    --init-base) INIT_BASE=true ;;
    --set-admin) SET_ADMIN=true ;;
  esac
done

if [ ! -d "$REPO_DIR" ]; then
  echo "[phase2] Clone du repo dans $REPO_DIR..."
  sudo mkdir -p "$(dirname "$REPO_DIR")"
  sudo git clone "$REPO_URL" "$REPO_DIR"
  sudo chown -R "$(whoami):$(whoami)" "$REPO_DIR"
fi

cd "$REPO_DIR"
echo "[phase2] Mise à jour du code..."
git pull origin main

echo "[phase2] Lancement Odoo + PostgreSQL..."
docker compose -f "$COMPOSE_FILE" up -d

if [ "$INIT_BASE" = true ]; then
  echo "[phase2] Initialisation de la base (module base)..."
  docker compose -f "$COMPOSE_FILE" run --rm odoo odoo -c "$ODOO_CONF" -d "$DB_NAME" -i base --stop-after-init --without-demo=all
  echo "[phase2] Redémarrage des conteneurs..."
  docker compose -f "$COMPOSE_FILE" up -d
fi

if [ "$SET_ADMIN" = true ]; then
  echo "[phase2] Définition de l'admin (techsupport@senegel.com)..."
  docker compose -f "$COMPOSE_FILE" run --rm odoo sh -c "cat /etc/odoo/set_admin_senegal.py | odoo shell -d $DB_NAME -c $ODOO_CONF --no-http"
fi

echo "[phase2] Terminé. Accès : http://IP_DU_VPS:8069"
