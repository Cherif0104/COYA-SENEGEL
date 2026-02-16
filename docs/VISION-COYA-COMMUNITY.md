# Vision & Guide d'implantation : Écosystème COYA Community

Document de référence pour aligner la plateforme COYA.PRO (Odoo 18) avec la stratégie de transformation digitale et managériale de l'ONG Sénégel — horizon 2026.

---

## 1. Vision stratégique

- **COYA** : Create Opportunity Youth of Africa — plateforme au service de la jeunesse africaine.
- **Objectif** : faire de COYA le « sanctuaire de la souveraineté » : outil maîtrisé, debrandé (sans identité éditeur), adapté aux valeurs et processus de Sénégel.
- **Pilier managérial** : la **Trinité** — équilibre entre **Productivité** (Ndiguel / discipline), **Profitabilité** (Barké / impact), **Professionnalisme** (Yar / éthique). Un pilier sous 30 % déclenche une intervention du Conseil de la Trinité. _(Note: Module Trinité mis en pause dans la V1, sera réintégré plus tard)_
- **Standards** : ISO 9001, méthodologies Agiles (SCRUM), objectifs SMART.

---

## 2. Charte graphique COYA

| Élément | Règle |
|--------|--------|
| **Nom plateforme** | COYA (Create Opportunity Youth of Africa) — affiché comme COYA.PRO / COYA Community. |
| **Couleurs** | **Émeraude Ndiguel** `#2E7D32` (discipline, boutons Valider) · **Ambre Yar** `#FF8F00` (éducation, alertes, qualité) · **Or Barké** `#FBC02D` (impact, récompenses). |
| **Typographie** | Police moderne et lisible (ex. Montserrat, Inter) pour un rendu professionnel international. |
| **Iconographie** | Éclair vert = productivité ; Micro doré = Xalima (voix). Remplacer les icônes génériques par ces symboles où pertinent. |
| **Identité** | Logo SENEGEL, slogan « CITOYENNETÉ, TRANSPARENCE, COMPÉTENCES », lien senegel.org. |

---

## 3. Stack technique (VPS)

| Composant | Choix |
|-----------|--------|
| **Serveur** | VPS Ubuntu 22.04 LTS (ex. Contabo Cloud VPS 10 ou supérieur). |
| **Application** | Odoo 18 Community Edition. |
| **Base de données** | PostgreSQL 15+ (sur le même VPS — option B Contabo, sans Supabase). |
| **Sécurité** | Nginx en reverse proxy + SSL Let's Encrypt. |
| **Add-ons** | Dossier dédié (ex. `addons/custom` = coya-addons) : branding, modules métier, OCA. |

Référence déploiement : `docker-compose.contabo.yml`, `docs/DEPLOI-CONTABO-STANDALONE.md`.

---

## 4. Modules opérationnels (cœur ONG)

### 4.1 Branding & debranding (white label)

- **sunugest_branding** (existant) : titre COYA.PRO, footer SENEGEL·COYA.PRO, login deux panneaux, charte.
- À renforcer / ajouter selon dispo Odoo 18 : modules type *remove powered by*, *mail_debrand*, *custom_branding* (onglet « COYA ERP », OdooBot → « Assistant COYA »).
- **web_responsive** (OCA) : interface fluide sur mobile pour les agents de terrain.

### 4.2 Gestion des ressources & projets (Agile)

- **project** (base) : tâches, Kanban.
- **project_agile_scrum** (Modoolar/OCA ou équivalent 18) : Sprints, Product Backlog, rôle Sage = Scrum Master.
- **ks_gantt_view_project** : Gantt, planification dans le temps.
- **zt_capacity_planning** (ou équivalent) : charge vs capacité, éviter surcharge des équipes.

### 4.3 RH & performance

- **hr_attendance** : pointage (Kiosk possible).
- **hr_attendance_geolocalize** : présence terrain.
- **hr_appraisal** (Community) : évaluations, objectifs SMART.
- **gamification** : défis, Jetons de Barké, Badges de Ngor, leaderboards.

### 4.4 Finances & transparence donateurs

- **account** + localisation OHADA / Sénégal (plan comptable sénégalais).
- **ngo_management_system** : liaison subventions (Grants) ↔ dépenses projets.
- **donation** (OCA) : donateurs, reçus, traçabilité dons (nature / financiers).

### 4.5 Qualité ISO 9001

- **mgmtsystem** (OCA) : audits internes, non-conformités, actions correctives, cycle PDCA.
- **document** : protocoles, SOP, gestion des versions.

### 4.6 Xalima (inclusion vocale)

- **pits_voice_to_text_chatter** (ou équivalent 18) : bouton micro dans le Chatter, dictée → texte.
- **audio_note** (si dispo) : notes vocales attachées aux enregistrements (projets, tâches).

### 4.7 Expansion & gouvernance

- **Multi-sociétés** (natif Odoo) : siège Dakar + antennes (Sénégal, Gambie, Guinée, etc.), journaux et devises par entité, consolidation.
- **kpi_dashboard** (ou vues custom) : tableau de bord Trinité (Productivité, Profitabilité, Professionnalisme), alertes, vue consolidée réseau. _(Note: Dashboard Trinité mis en pause dans la V1)_

---

## 5. Ordre de déploiement recommandé (2026)

1. **Branding complet & identité** — Charte (couleurs, typo, icônes), debranding renforcé, web_responsive.
2. **Fondations** — Multi-sociétés, Comptabilité + localisation OHADA/Sénégal.
3. **Projets & Agile** — project + project_agile_scrum, capacity planning, Gantt.
4. **ISO 9001** — mgmtsystem, document (SOP, audits, non-conformités).
5. **RH & performance** — hr_attendance, hr_appraisal, gamification (Barké, Ngor).
6. **Finances ONG** — ngo_management_system, donation, budgets analytiques.
7. **Xalima** — voice-to-text Chatter, audio_note.
8. **Dashboard Trinité** — KPI Productivité / Profitabilité / Professionnalisme, consolidation multi-sociétés. _(Note: Mis en pause dans la V1)_

---

## 6. Références

- Stratégie globale : document « Stratégie Globale de Transformation Digitale et Managériale — COYA Community ».
- Guide d’implantation : « Guide d’Implantation Stratégique : Écosystème COYA Community » (charte, modules, stack).
- Déploiement VPS : `docs/DEPLOI-CONTABO-STANDALONE.md`, `docs/DEPLOI-VPS-OVH-CONTABO.md`.
- Conventions OCA : [OCA Contributing](https://github.com/OCA/odoo-community.org/blob/master/website/Contribution/CONTRIBUTING.rst).
- Odoo 18 : édition Community, personnalisation et modules compatibles 18.

---

---

## 7. Implantation déjà appliquée (codebase)

- **Charte graphique** : couleurs Trinité (Émeraude #2E7D32, Ambre #FF8F00, Or #FBC02D) et typographie Montserrat/Inter dans `addons/custom/sunugest_branding/static/src/scss/sunugest_theme.scss`.
- **Debranding** : titre onglet « COYA ERP · SENEGEL », footer « SENEGEL · COYA.PRO », login deux panneaux, page hors ligne aux couleurs COYA.
- **Stack** : `docker-compose.contabo.yml` (option B sans Supabase), `docs/DEPLOI-CONTABO-STANDALONE.md`.

Les modules opérationnels (Agile, ISO, Xalima, etc.) restent à installer et configurer selon les phases 2 à 8.

---

## 8. Vision par département et par module (référence managériale)

Organisation de la plateforme par **départements** et **modules fonctionnels / opérationnels**, avec une approche de gestion orientée performance, qualité et transparence.

### 8.1 Comptabilité : deux niveaux distincts

| Niveau | Objet | Odoo / modules |
|--------|--------|-----------------|
| **Comptabilité d’entreprise** | Charges, dépenses, achats, trésorerie, paie, TVA, bilans | `account`, `purchase`, `hr_expense`, `hr_payroll`, PCE / OHADA |
| **Comptabilité programmes & projets (bailleurs)** | Budgets alloués par bailleur, lignes budgétaires, imputation par projet, prévisionnel vs réel, justificatifs, rapports bailleur | Module dédié « Comptabilité analytique programmes » : programmes → projets → lignes → imputation dépenses → rapports |

**Innovation cible** : un module **Comptabilité analytique programmes** qui garde les écritures dans la compta entreprise tout en gérant programmes / projets / lignes budgétaires, imputation des dépenses et rapports par bailleur (prévisionnel vs réel, justificatifs).

---

### 8.2 Départements et modules

#### Administratif & financier
- Compta entreprise, compta programmes, trésorerie, achats, documents administratifs, contrats & engagements.
- **Innovation** : Dossier projet financier (budget, dépenses, justificatifs, rapports bailleur).

#### Juridique
- Risques juridiques, contrats, conformité, contentieux.
- **Innovation** : Tableau de bord juridique (risques, contrats à renouveler, contentieux, conformité).

#### Audiovisuel / Production
- Projets de production, équipes, matériel, planning, livrables, budget production.
- **Innovation** : Studio board (Kanban : idée → script → tournage → postprod → diffusion).

#### Formation & Bootcamp
- Bootcamps, cohortes, formateurs, participants, fiches de collecte, portail apprenants, évaluation formation.
- **Innovation** : Parcours apprenant (inscription → certification, lien Trinité).

#### RH
- Employés, paie, congés, présence, performance, recrutement, politiques RH.
- **Innovation** : Fiche RH enrichie Trinité (scores Ndiguel / Barké / Yar intégrés à la fiche employé et à l’évaluation).

#### Project Management (Programmes & Projets)
- Programmes, projets, budget prévisionnel / réel, rapprochement, tâches, équipe projet, reporting bailleur.
- **Innovation** : Ligne budgétaire intelligente (budget, engagé, payé, restant, justificatifs par ligne).

#### Prospection & Partenariat
- Partenaires, opportunités, pipeline, engagements, suivi relationnel.
- **Innovation** : Carte des partenaires (vue par type / secteur / engagement, alertes).

#### Conseil consultatif (Gouvernance)
- Tableau de bord stratégique, activités & réalisations, décisions, documents de gouvernance, alertes.
- **Innovation** : Conseil board (tableau de bord temps réel pour administrateurs).

#### Qualité & Suivi performance
- Trinité (noyau), audits internes, contrôles, notation transversale, indicateurs qualité, plans d’action.
- **Innovation** : Score qualité global (agrégation Trinité + audits + contrôles par département / personne).

#### IT & Tech Solutions
- Projets techniques, solutions / produits, support, infrastructure, documentation.
- **Innovation** : Tech pipeline (cycle de vie : idée → POC → dev → production → maintenance).

#### Trinité (transversal)
- Productivité (Ndiguel), Profitabilité (Barké), Professionnalisme (Yar) — présents dans tous les départements.
- Lien RH : alimentation évaluation, paie variable, plan de formation, évolution de carrière.

---

### 8.3 Priorisation (suite aux phases 1–8)

1. **Court terme** : Déblocage Trinité (RelaxNG), intégration Trinité ↔ RH, droits par département (groupes / rôles).
2. **Moyen terme** : Compta programmes, module Project Management (budget, rapprochement, justificatifs).
3. **Long terme** : Qualité & suivi performance, Conseil consultatif, Prospection, IT.

---

*Dernière mise à jour : février 2026 — Projet COYA.PRO / SENEGEL.*
