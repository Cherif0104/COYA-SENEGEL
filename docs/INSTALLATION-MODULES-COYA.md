# Installation des modules COYA — GitHub et VPS

## 1. Pousser les modifications (déjà fait)

Les modifications ont été poussées sur GitHub (branche `main`).

---

## 2. Déployer sur le VPS (Contabo)

### Depuis votre poste (PowerShell ne gère pas `cd /opt/...`)

Connectez-vous au VPS en SSH, puis exécutez les commandes **sur le serveur** :

```bash
# 1. Connexion SSH au VPS
ssh root@5.189.175.90

# 2. Aller dans le répertoire du projet
cd /opt/COYA-SENEGEL

# 3. Lancer le script de déploiement (pull + mise à jour des modules + redémarrage Odoo)
bash scripts/deploy_contabo.sh
```

Le script va :
- faire un `git pull origin main`
- mettre à jour les modules : sunugest_branding, coya_modern_navbar, coya_planning, coya_time_tracking, coya_trinite, coya_collecte, coya_bootcamp
- redémarrer le conteneur Odoo

### Si vous préférez faire les étapes à la main

```bash
ssh root@5.189.175.90
cd /opt/COYA-SENEGEL

git pull origin main

# Mise à jour de tous les modules custom
docker compose -f docker-compose.contabo.yml run --rm odoo odoo \
  -c /etc/odoo/odoo-standalone.conf \
  -u sunugest_branding,coya_modern_navbar,coya_planning,coya_time_tracking,coya_trinite,coya_collecte,coya_bootcamp \
  -d postgres \
  --stop-after-init

# Redémarrer Odoo
docker compose -f docker-compose.contabo.yml restart odoo
```

---

## 3. Installer les nouveaux modules (première fois)

Si les modules **coya_planning**, **coya_time_tracking**, **coya_trinite**, **coya_collecte**, **coya_bootcamp** ne sont pas encore installés sur la base :

1. Dans Odoo : **Paramètres** → **Applications** → **Mettre à jour la liste des applications**.
2. Rechercher et installer **dans cet ordre** (à cause des dépendances) :
   - **COYA Planning**
   - **COYA Time Tracking** (dépend : hr, hr_attendance, coya_planning, project)
   - **COYA Trinité** (dépend : hr, coya_planning, coya_time_tracking)
   - **COYA Collecte**
   - **COYA Bootcamp** (dépend : coya_collecte)

### Prérequis Odoo

Pour que tous les modules fonctionnent, les applications Odoo suivantes doivent être installées :

- **Employés** (hr)
- **Présence** (hr_attendance)
- **Calendrier** (calendar)
- **Projets** (project) — nécessaire pour COYA Time Tracking

Si une dépendance manque, Odoo proposera de l’installer lors de l’installation du module.

---

## 4. Résumé des modules déployés

| Module | Rôle |
|--------|------|
| **sunugest_branding** | Charte COYA, page de login deux panneaux |
| **coya_modern_navbar** | Sidebar, dashboard, menus |
| **coya_planning** | Créneaux de planification (réunions, télétravail, terrain, etc.) |
| **coya_time_tracking** | Suivi du temps, entrées de temps |
| **coya_trinite** | Plans de paie, scores Ndiguel/Barké/Yar, alertes, dashboard Trinité |
| **coya_collecte** | Types de fiches, formulaires publics avec lien partageable |
| **coya_bootcamp** | Bootcamps, cohortes, intervenants, participants |

---

## 5. Après déploiement

- **Login** : page deux panneaux (gauche formulaire, droite bienvenue + Trinité).
- **Formulaires publics** : `https://VOTRE-DOMAINE/coya/fiche/<ID_TYPE_FICHE>` (sans connexion).
- **Menus** : Planification, Suivi du temps, Trinité, Collecte, Bootcamps dans la sidebar (section RH / Business selon le nom).

*Dernière mise à jour : février 2026 — COYA.PRO / SENEGEL.*
