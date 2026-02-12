# Vision & Guide d'implantation : Écosystème COYA Community

Document de référence pour aligner la plateforme COYA.PRO (Odoo 18) avec la stratégie de transformation digitale et managériale de l'ONG Sénégel — horizon 2026.

---

## 1. Vision stratégique

- **COYA** : Create Opportunity Youth of Africa — plateforme au service de la jeunesse africaine.
- **Objectif** : faire de COYA le « sanctuaire de la souveraineté » : outil maîtrisé, debrandé (sans identité éditeur), adapté aux valeurs et processus de Sénégel.
- **Pilier managérial** : la **Trinité** — équilibre entre **Productivité** (Ndiguel / discipline), **Profitabilité** (Barké / impact), **Professionnalisme** (Yar / éthique). Un pilier sous 30 % déclenche une intervention du Conseil de la Trinité.
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
- **kpi_dashboard** (ou vues custom) : tableau de bord Trinité (Productivité, Profitabilité, Professionnalisme), alertes, vue consolidée réseau.

---

## 5. Ordre de déploiement recommandé (2026)

1. **Branding complet & identité** — Charte (couleurs, typo, icônes), debranding renforcé, web_responsive.
2. **Fondations** — Multi-sociétés, Comptabilité + localisation OHADA/Sénégal.
3. **Projets & Agile** — project + project_agile_scrum, capacity planning, Gantt.
4. **ISO 9001** — mgmtsystem, document (SOP, audits, non-conformités).
5. **RH & performance** — hr_attendance, hr_appraisal, gamification (Barké, Ngor).
6. **Finances ONG** — ngo_management_system, donation, budgets analytiques.
7. **Xalima** — voice-to-text Chatter, audio_note.
8. **Dashboard Trinité** — KPI Productivité / Profitabilité / Professionnalisme, consolidation multi-sociétés.

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

*Dernière mise à jour : février 2026 — Projet COYA.PRO / SENEGEL.*
