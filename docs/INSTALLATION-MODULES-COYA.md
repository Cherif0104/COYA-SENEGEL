# Installation des modules COYA (Odoo 18)

Guide pour installer et mettre à jour les modules custom COYA sur une instance Odoo 18.

---

## 1. Liste des modules custom

| Module | Résumé | Dépendances Odoo / COYA |
|--------|--------|--------------------------|
| **sunugest_branding** | Identité COYA.PRO, charte, debrand (titre, footer, login) | `web`, `mail` |
| **coya_departments** | Groupes et menus racine par département (Administratif, Juridique, Formation, RH, etc.) | `base` |
| **coya_modern_navbar** | Navbar gauche, écran d'accueil, section COYA en premier | `web`, `base` |
| **coya_collecte** | Formulaires publics modulables (fiches, types, réponses) | `base`, `web`, `coya_departments` |
| **coya_planning** | Planification (réunions, télétravail, bureau, terrain, formations) | `hr`, `calendar`, `coya_departments` |
| **coya_time_tracking** | Suivi du temps (pointage, types d'activité, lien projets) | `hr`, `hr_attendance`, `coya_planning`, `project` |
| **coya_trinite** | Plans de paie, scores Trinité (Ndiguel, Barké, Yar), alertes Conseil | `hr`, `coya_planning`, `coya_time_tracking`, `coya_departments` |
| **coya_bootcamp** | Bootcamps, cohortes, intervenants, participants, parcours apprenant | `base`, `coya_collecte`, `coya_departments` |
| **coya_programme_budget** | Compta programmes (programmes, projets, lignes budgétaires, imputations, rapport bailleur) | `base`, `coya_departments` |
| **coya_juridique** | Risques juridiques, contrats, contentieux | `base`, `coya_departments` |
| **coya_studio** | Studio board (Kanban production : idée → script → tournage → postprod → diffusion) | `base`, `coya_departments`, `hr` |
| **coya_partenariat** | Carte des partenaires, opportunités (pipeline) | `base`, `coya_departments` |
| **coya_conseil** | Tableau de bord Conseil (gouvernance) | `web`, `base`, `coya_departments` |
| **coya_qualite** | Score qualité global (Trinité + audits + contrôles) | `base`, `coya_departments`, `coya_trinite`, `hr` |
| **coya_tech** | Pipeline Tech (idée → POC → dev → production → maintenance) | `base`, `coya_departments` |
| **coya_programme_budget_project** | Lien Projet Odoo sur les projets compta programmes | `coya_programme_budget`, `project` |
| **coya_tech_project** | Lien Projet Odoo sur les projets Tech | `coya_tech`, `project` |
| **coya_hr_trinite_appraisal** | Scores Trinité sur la fiche d'évaluation RH | `coya_trinite`, `hr_appraisal` |

---

## 2. Ordre d'installation recommandé

Les modules doivent être installés en respectant les dépendances. Ordre suggéré :

1. **Fondations**
   - `sunugest_branding`
   - `coya_departments`

2. **Collecte et Planification**
   - `coya_collecte`
   - `coya_planning` (nécessite `hr`, `calendar`)

3. **Time tracking et Trinité**
   - `coya_time_tracking` (nécessite `hr_attendance`, `project`)
   - `coya_trinite`

4. **Formation, Compta programmes, autres départements**
   - `coya_bootcamp`
   - `coya_programme_budget`
   - `coya_juridique`
   - `coya_studio`
   - `coya_partenariat`
   - `coya_conseil`
   - `coya_qualite`
   - `coya_tech`

5. **Optionnels**
   - `coya_modern_navbar` (à tout moment, dépend seulement de `web`, `base`)
   - `coya_programme_budget_project` et `coya_tech_project` : uniquement si le module **Projet** (`project`) est installé et que vous souhaitez lier les projets COYA aux projets Odoo.
   - `coya_hr_trinite_appraisal` : uniquement si le module **Évaluations** (`hr_appraisal`) est installé ; affiche les scores Trinité (Ndiguel, Barké, Yar) sur la fiche d'évaluation de l'employé.

**Note** : `coya_programme_budget` et `coya_tech` **n'exigent plus** le module `project`. Pour avoir le champ « Projet Odoo » sur les projets (compta programmes ou tech), installer en plus les modules pont `coya_programme_budget_project` et/ou `coya_tech_project`.

---

## 3. Configuration post-installation

- **Groupes COYA Départements** : Dans **Paramètres > Utilisateurs**, pour chaque utilisateur, attribuer au moins un groupe sous la catégorie **COYA Départements** (ex. « Formation & Bootcamp », « RH », « Qualité & Suivi performance »). Sans cela, les menus rattachés (Trinité, Bootcamps, Collecte, Planification, etc.) ne seront pas visibles pour cet utilisateur.
- **Rapport bailleur** : Depuis **COYA > Administratif & Financier > Compta programmes > Programmes**, le bouton **Imprimer** permet d’imprimer le **Rapport bailleur** (prévisionnel vs réel) pour le(s) programme(s) sélectionné(s).

- **Debranding (OdooBot → Assistant COYA)** : Après l'installation ou la mise à jour du module **COYA.PRO Branding** (`sunugest_branding`), le bot système utilisé dans Discuss, Chatter et les notifications est renommé automatiquement de « OdooBot » à « Assistant COYA ». Ce renommage est effectué par un hook exécuté au chargement du module. Si, après une mise à jour majeure d'Odoo, le bot réapparaît sous le nom « OdooBot », mettre à jour à nouveau le module `sunugest_branding` pour réappliquer le renommage.

---

## 4. Mise à jour des modules

Après modification du code des addons, mettre à jour les modules concernés depuis **Applications** (mode développeur) ou en ligne de commande :

```bash
odoo -u module_name -d ma_base --stop-after-init
```

Pour mettre à jour tous les modules COYA, mettre à jour les modules « feuilles » (sans dépendants custom) puis remonter ; ou mettre à jour chaque module listé ci-dessus dans l’ordre inverse des dépendances.

---

## 5. Checklist déploiement (premier déploiement / mise en production)

1. Installer les modules COYA selon l'ordre de la section 2.
2. Attribuer les groupes COYA Départements aux utilisateurs (section 3).
3. Vérifier le debranding : titre de l'onglet, footer, OdooBot → Assistant COYA (après mise à jour de `sunugest_branding`).
4. (Optionnel) Installer et configurer les modules tiers selon la vision (compta OHADA, project, hr_attendance, etc.) — voir [VISION-COYA-COMMUNITY.md](docs/VISION-COYA-COMMUNITY.md), section 5.

---

*Dernière mise à jour : février 2026 — Projet COYA.PRO / SENEGEL.*
