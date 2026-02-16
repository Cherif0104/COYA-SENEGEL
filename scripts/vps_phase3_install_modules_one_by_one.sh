#!/usr/bin/env bash
# Phase 3 : Installation des modules COYA un par un (ordre de docs/INSTALLATION-MODULES-COYA.md)
# À exécuter sur le VPS après phase 2 (base initialisée).
# Usage: bash vps_phase3_install_modules_one_by_one.sh
# Pour n'installer que les modules obligatoires (sans optionnels), passez SKIP_OPTIONAL=1

set -e
REPO_DIR="${REPO_DIR:-/opt/COYA-SENEGEL}"
COMPOSE_FILE="docker-compose.contabo.yml"
ODOO_CONF="/etc/odoo/odoo-standalone.conf"
DB_NAME="postgres"

# Ordre section 2 : Fondations → Collecte/Planification → Time/Trinité → Reste → Optionnels
MODULES_CORE=(
  sunugest_branding
  coya_departments
  coya_collecte
  coya_planning
  coya_time_tracking
  coya_trinite
  coya_bootcamp
  coya_programme_budget
  coya_juridique
  coya_studio
  coya_partenariat
  coya_conseil
  coya_qualite
  coya_tech
)
MODULES_OPTIONAL=(
  coya_modern_navbar
  coya_programme_budget_project
  coya_tech_project
  coya_hr_trinite_appraisal
)

cd "$REPO_DIR"

for mod in "${MODULES_CORE[@]}"; do
  echo "[phase3] Installation de $mod..."
  docker compose -f "$COMPOSE_FILE" run --rm odoo odoo -c "$ODOO_CONF" -d "$DB_NAME" -i "$mod" --stop-after-init
done

if [ "${SKIP_OPTIONAL:-0}" != "1" ]; then
  for mod in "${MODULES_OPTIONAL[@]}"; do
    echo "[phase3] Installation optionnelle de $mod..."
    docker compose -f "$COMPOSE_FILE" run --rm odoo odoo -c "$ODOO_CONF" -d "$DB_NAME" -i "$mod" --stop-after-init || true
  done
fi

echo "[phase3] Redémarrage Odoo..."
docker compose -f "$COMPOSE_FILE" restart odoo

echo "[phase3] Terminé. Appliquer la checklist section 5 (groupes COYA Départements, debranding)."
