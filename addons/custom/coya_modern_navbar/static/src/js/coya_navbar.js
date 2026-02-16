/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { NavBar } from "@web/webclient/navbar/navbar";
import { Component, onMounted, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { user } from "@web/core/user";
import { browser } from "@web/core/browser/browser";

/**
 * Patch de la NavBar Odoo pour masquer la navbar par défaut et injecter notre sidebar
 */
patch(NavBar.prototype, {
    setup() {
        super.setup();
        onMounted(() => {
            this.injectCoyaSidebar();
        });
    },

    injectCoyaSidebar() {
        // Masquer la navbar Odoo
        const navbar = document.querySelector(".o_main_navbar");
        if (navbar) {
            navbar.style.display = "none";
        }

        // Vérifier si la sidebar existe déjà
        if (document.getElementById("coya-sidebar")) {
            return;
        }

        // Créer la sidebar
        const sidebar = document.createElement("div");
        sidebar.id = "coya-sidebar";
        sidebar.className = "coya-sidebar";
        sidebar.innerHTML = `
            <div class="coya-sidebar-brand">
                <div class="coya-sidebar-logo">
                    <img src="/sunugest_branding/static/img/logo_senegel.png" alt="COYA.PRO"/>
                </div>
                <span class="coya-sidebar-brand-text">COYA.PRO</span>
            </div>
            <nav class="coya-sidebar-nav" id="coya-sidebar-nav">
                <!-- Sections injectées par JS (Core, Business, Opérations, RH, etc.) -->
            </nav>
        `;

        // Injecter la sidebar au début du body
        document.body.insertBefore(sidebar, document.body.firstChild);

        // Header / Leader (bienvenue, user, date/heure, pointage, Paramètres, Aide)
        this.injectCoyaHeader();

        // Ajuster le contenu principal
        const actionManager = document.querySelector(".o_action_manager");
        if (actionManager) {
            actionManager.classList.add("coya-main-content");
        }

        // Charger les apps dans la sidebar
        this.loadAppsInSidebar();
    },

    injectCoyaHeader() {
        if (document.getElementById("coya-leader")) return;

        const userName = user.name || user.login || "Utilisateur";
        const presenceKey = "coya_presence_status";
        const savedPresence = browser.localStorage.getItem(presenceKey) || "online";

        const header = document.createElement("header");
        header.id = "coya-leader";
        header.className = "coya-leader";
        const initial = (userName || "U").charAt(0).toUpperCase();
        header.innerHTML = `
            <div class="coya-leader-inner">
                <div class="coya-leader-left">
                    <p class="coya-leader-welcome">Bienvenue dans l'espace de travail SENEGEL</p>
                    <p class="coya-leader-user">
                        <span class="coya-leader-name">${userName}</span>
                        <span class="coya-leader-meta" id="coya-leader-role"></span>
                        <span class="coya-leader-meta" id="coya-leader-department"></span>
                    </p>
                    <p class="coya-leader-datetime" id="coya-leader-datetime"></p>
                </div>
                <div class="coya-leader-center">
                    <input type="search" class="coya-leader-search" id="coya-leader-search" placeholder="Rechercher menu, action..." aria-label="Recherche globale"/>
                </div>
                <div class="coya-leader-right">
                    <div class="coya-leader-presence">
                        <span class="coya-presence-timer" id="coya-presence-timer" title="Temps travaillé aujourd'hui">0h 00m</span>
                        <span class="coya-presence-label">Statut :</span>
                        <div class="coya-presence-dropdown">
                            <button type="button" class="coya-presence-btn" id="coya-presence-btn" data-status="${savedPresence}" title="Cliquez pour pointer / changer le statut">
                                <span class="coya-presence-dot coya-presence-${savedPresence}"></span>
                                <span class="coya-presence-text" id="coya-presence-text">${this.getPresenceLabel(savedPresence)}</span>
                                <i class="fa fa-chevron-down"></i>
                            </button>
                            <div class="coya-presence-menu" id="coya-presence-menu">
                                <button type="button" data-status="online"><span class="dot online"></span> En ligne</button>
                                <button type="button" data-status="lunch"><span class="dot lunch"></span> Post-déjeuner</button>
                                <button type="button" data-status="meeting"><span class="dot meeting"></span> En réunion</button>
                                <button type="button" data-status="absent"><span class="dot absent"></span> Absent</button>
                            </div>
                        </div>
                    </div>
                    <button type="button" class="coya-leader-icon-btn" id="coya-leader-notif" title="Notifications" aria-label="Notifications">
                        <i class="fa fa-bell"></i>
                        <span class="coya-notif-dot" id="coya-notif-dot" style="display: none;"></span>
                    </button>
                    <a href="#" class="coya-leader-link" data-menu-xmlid="base.menu_administration" title="Paramètres">
                        <i class="fa fa-cog"></i> Paramètres
                    </a>
                    <a href="#" class="coya-leader-link" data-menu-xmlid="base.menu_help" title="Aide">
                        <i class="fa fa-question-circle"></i> Aide
                    </a>
                    <div class="coya-leader-profile">
                        <button type="button" class="coya-leader-profile-btn" id="coya-leader-profile-btn" title="Profil">
                            <span class="coya-avatar">${initial}</span>
                            <span class="coya-leader-profile-name">${userName}</span>
                            <i class="fa fa-chevron-down" style="font-size: 0.75rem;"></i>
                        </button>
                        <div class="coya-leader-profile-menu" id="coya-leader-profile-menu">
                            <a href="/web/session/logout"><i class="fa fa-sign-out"></i> Déconnexion</a>
                        </div>
                    </div>
                </div>
            </div>
        `;

        const webClient = document.querySelector(".o_web_client");
        if (webClient) {
            webClient.insertBefore(header, webClient.firstChild);
        }

        this.setupCoyaHeader(presenceKey);
    },

    getPresenceLabel(status) {
        const labels = { online: "En ligne", lunch: "Post-déjeuner", meeting: "En réunion", absent: "Absent" };
        return labels[status] || "En ligne";
    },

    setupCoyaHeader(presenceKey) {
        const menuService = this.env.services.menu;
        const actionService = this.env.services.action;

        // Date/heure (rafraîchie chaque minute)
        const updateDateTime = () => {
            const el = document.getElementById("coya-leader-datetime");
            if (el) {
                const now = new Date();
                el.textContent = now.toLocaleDateString("fr-FR", { weekday: "short", day: "numeric", month: "short", year: "numeric" }) + " — " + now.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" });
            }
        };
        updateDateTime();
        setInterval(updateDateTime, 60000);

        // Time tracking — temps travaillé aujourd'hui (depuis la connexion)
        const COYA_DAY_KEY = "coya_work_date";
        const COYA_SECONDS_KEY = "coya_work_seconds";
        const today = new Date().toISOString().slice(0, 10);
        let storedAtLoad = parseInt(browser.localStorage.getItem(COYA_SECONDS_KEY) || "0", 10);
        if (browser.localStorage.getItem(COYA_DAY_KEY) !== today) {
            storedAtLoad = 0;
            browser.localStorage.setItem(COYA_DAY_KEY, today);
        }
        const sessionStart = Date.now();
        const formatWorkTime = (totalSeconds) => {
            const h = Math.floor(totalSeconds / 3600);
            const m = Math.floor((totalSeconds % 3600) / 60);
            return `${h}h ${String(m).padStart(2, "0")}m`;
        };
        const updateWorkTimer = () => {
            const el = document.getElementById("coya-presence-timer");
            if (el) {
                const elapsedThisSession = (Date.now() - sessionStart) / 1000;
                const totalToday = storedAtLoad + elapsedThisSession;
                el.textContent = formatWorkTime(totalToday);
            }
        };
        updateWorkTimer();
        const workTimerInterval = setInterval(updateWorkTimer, 1000);
        const saveWorkTime = () => {
            const elapsed = (Date.now() - sessionStart) / 1000;
            const total = storedAtLoad + elapsed;
            browser.localStorage.setItem(COYA_SECONDS_KEY, String(Math.round(total)));
        };
        window.addEventListener("beforeunload", saveWorkTime);
        document.addEventListener("visibilitychange", () => {
            if (document.visibilityState === "hidden") saveWorkTime();
        });

        // Rôle / Département (RPC optionnel)
        this.loadUserRoleDepartment();

        // Dropdown présence
        const btn = document.getElementById("coya-presence-btn");
        const menu = document.getElementById("coya-presence-menu");
        if (btn && menu) {
            btn.addEventListener("click", (e) => {
                e.stopPropagation();
                menu.classList.toggle("show");
            });
            document.addEventListener("click", () => menu.classList.remove("show"));
            menu.querySelectorAll("button[data-status]").forEach((opt) => {
                opt.addEventListener("click", (e) => {
                    e.stopPropagation();
                    const status = opt.dataset.status;
                    browser.localStorage.setItem(presenceKey, status);
                    btn.dataset.status = status;
                    btn.querySelector(".coya-presence-dot").className = "coya-presence-dot coya-presence-" + status;
                    document.getElementById("coya-presence-text").textContent = this.getPresenceLabel(status);
                    menu.classList.remove("show");
                });
            });
        }

        // Paramètres / Aide
        document.querySelectorAll(".coya-leader a.coya-leader-link[data-menu-xmlid]").forEach((link) => {
            link.addEventListener("click", async (e) => {
                e.preventDefault();
                const xmlid = link.getAttribute("data-menu-xmlid");
                const allMenus = menuService.getAll();
                const menu = allMenus.find((m) => m.xmlid === xmlid);
                if (menu && menu.actionID) {
                    await menuService.selectMenu(menu);
                }
            });
        });

        // Recherche globale : filtrer et ouvrir un menu
        const searchEl = document.getElementById("coya-leader-search");
        if (searchEl) {
            searchEl.addEventListener("keydown", (e) => {
                if (e.key === "Enter") {
                    e.preventDefault();
                    const q = searchEl.value.trim().toLowerCase();
                    if (!q) return;
                    const allMenus = menuService.getAll();
                    const match = allMenus.find((m) => m.name && m.name.toLowerCase().includes(q));
                    if (match && match.actionID) {
                        actionService.doAction(match.actionID);
                        searchEl.value = "";
                    }
                }
            });
        }

        // Notifications (placeholder)
        const notifBtn = document.getElementById("coya-leader-notif");
        if (notifBtn) {
            notifBtn.addEventListener("click", () => {
                const allMenus = menuService.getAll();
                const discuss = allMenus.find((m) => m.name && (m.name.toLowerCase().includes("discussion") || m.name.toLowerCase().includes("discuss")));
                if (discuss && discuss.actionID) actionService.doAction(discuss.actionID);
            });
        }

        // Profil dropdown
        const profileBtn = document.getElementById("coya-leader-profile-btn");
        const profileMenu = document.getElementById("coya-leader-profile-menu");
        if (profileBtn && profileMenu) {
            profileBtn.addEventListener("click", (e) => {
                e.stopPropagation();
                profileMenu.classList.toggle("show");
            });
            document.addEventListener("click", () => profileMenu.classList.remove("show"));
        }
    },

    async loadUserRoleDepartment() {
        const roleEl = document.getElementById("coya-leader-role");
        const deptEl = document.getElementById("coya-leader-department");
        if (!roleEl && !deptEl) return;
        try {
            const orm = this.env.services.orm;
            const [userData] = await orm.read("res.users", [user.userId], ["partner_id"]);
            if (roleEl) {
                roleEl.textContent = user.isAdmin ? " — Administrateur" : " — Utilisateur";
            }
            if (userData && userData.partner_id && deptEl) {
                const [partner] = await orm.read("res.partner", [userData.partner_id[0]], ["name"]).catch(() => []);
                try {
                    const [partnerExtra] = await orm.read("res.partner", [userData.partner_id[0]], ["department_id", "job_id"]).catch(() => []);
                    if (partnerExtra) {
                        if (partnerExtra.department_id) deptEl.textContent = " — " + (partnerExtra.department_id[1] || "");
                        if (partnerExtra.job_id && roleEl) roleEl.textContent = " — " + (partnerExtra.job_id[1] || "");
                    }
                } catch (_) {}
            }
        } catch (_e) {
            if (roleEl) roleEl.textContent = user.isAdmin ? " — Administrateur" : "";
        }
    },

    /** Mapping des apps Odoo vers sections sidebar (ERP moderne) */
    getSidebarSectionForApp(appName) {
        const n = (appName || "").toLowerCase();
        if (n.includes("coya")) return "COYA";
        if (n.includes("accueil") || n.includes("home") || n.includes("discussion") || n.includes("discuss") || n.includes("calendrier") || n.includes("calendar") || n.includes("to-do") || n.includes("todo") || n.includes("tâches")) return "Core";
        if (n.includes("crm") || n.includes("ventes") || n.includes("sale") || n.includes("facturation") || n.includes("invoic") || n.includes("projet") || n.includes("project") || n.includes("feuille") || n.includes("timesheet")) return "Business";
        if (n.includes("achat") || n.includes("purchase") || n.includes("inventaire") || n.includes("stock") || n.includes("dépense") || n.includes("expense")) return "Opérations";
        if (n.includes("employé") || n.includes("employee") || n.includes("présence") || n.includes("attendance") || n.includes("recrutement") || n.includes("recruit") || n.includes("congé") || n.includes("leave") || n.includes("déjeuner") || n.includes("lunch") || n.includes("hr ") || n === "hr" || n.includes("planification") || n.includes("trinité") || n.includes("suivi du temps") || n.includes("collecte") || n.includes("bootcamp")) return "RH";
        if (n.includes("événement") || n.includes("event") || n.includes("sondage") || n.includes("survey")) return "Marketing";
        if (n.includes("app") || n.includes("paramètre") || n.includes("setting") || n.includes("administration")) return "Système";
        return "Business";
    },

    loadAppsInSidebar() {
        const menuService = this.env.services.menu;
        const actionService = this.env.services.action;
        const nav = document.getElementById("coya-sidebar-nav");
        if (!nav) return;

        try {
            const apps = menuService.getApps();
            const sorted = [...apps].sort((a, b) => (a.sequence ?? 9999) - (b.sequence ?? 9999));

            const sectionOrder = ["COYA", "Core", "Business", "Opérations", "RH", "Marketing", "Système"];
            const sectionLabels = { COYA: "COYA", Core: "Principal", Business: "Business", Opérations: "Opérations", RH: "RH", Marketing: "Marketing", Système: "Système" };
            const bySection = {};
            sectionOrder.forEach((s) => (bySection[s] = []));
            sorted.forEach((app) => {
                const section = this.getSidebarSectionForApp(app.name);
                if (bySection[section]) bySection[section].push(app);
                else bySection["Business"].push(app);
            });

            nav.innerHTML = sectionOrder
                .filter((section) => bySection[section].length > 0)
                .map(
                    (section) => {
                        const label = sectionLabels[section] || section;
                        const items = bySection[section]
                            .map((app) => {
                                const iconClass = (app.webIcon || "fa fa-cube").split(",")[1] || "fa fa-cube";
                                const actionId = app.actionID || "";
                                return `
                            <li class="coya-nav-item">
                                <a href="#" class="coya-nav-link" data-action-id="${actionId}" data-menu-id="${app.id}">
                                    <i class="${iconClass}" aria-hidden="true"></i>
                                    <span class="coya-nav-text">${app.name}</span>
                                </a>
                            </li>`;
                            })
                            .join("");
                        return `
                    <div class="coya-nav-section">
                        <div class="coya-nav-section-title">${label}</div>
                        <ul class="coya-nav-list">${items}</ul>
                    </div>`;
                    }
                )
                .join("");

            nav.querySelectorAll(".coya-nav-link").forEach((link) => {
                link.addEventListener("click", (e) => {
                    e.preventDefault();
                    const actionId = link.dataset.actionId;
                    const menuId = link.dataset.menuId;
                    if (actionId) {
                        actionService.doAction(parseInt(actionId, 10));
                    } else if (menuId) {
                        menuService.selectMenu(parseInt(menuId, 10));
                    }
                    nav.querySelectorAll(".coya-nav-link").forEach((l) => l.classList.remove("active"));
                    link.classList.add("active");
                });
            });
        } catch (error) {
            console.error("Erreur chargement apps sidebar:", error);
        }
    },

});

/**
 * Client Action : Tableau de bord d'accueil COYA
 * — Regroupement par domaine (application racine), raccourcis + zones widgets (KPI/graphiques à brancher).
 * — Droits : uniquement ce que le backend renvoie (menu déjà filtré).
 */
export class CoyaHomeDashboard extends Component {
    setup() {
        this.menuService = useService("menu");
        this.actionService = useService("action");
        this.orm = useService("orm");
        this.state = useState({
            kpis: [],
            insights: [],
            tasks: [],
            actionsDue: [],
            suggestions: [],
            userIndicators: [],
            leaves: [],
            meetings: [],
            activity: [],
            loading: true,
        });

        onMounted(() => {
            this.loadDashboard();
        });
    }

    async loadDashboard() {
        try {
            await Promise.all([
                this.loadKpis(),
                this.loadInsights(),
                this.loadTasks(),
                this.loadActionsDue(),
                this.loadSuggestions(),
                this.loadUserIndicators(),
                this.loadLeaves(),
                this.loadMeetings(),
                this.loadGlobalActivity(),
            ]);
        } catch (error) {
            console.error("Erreur chargement dashboard:", error);
        } finally {
            this.state.loading = false;
        }
    }

    /** Alertes métier */
    async loadInsights() {
        const insights = [];
        try {
            const orm = this.orm;
            const draftCount = await orm.searchCount("sale.order", [["state", "=", "draft"]]).catch(() => 0);
            if (draftCount > 0) insights.push({ id: "draft_so", type: "warning", title: "Commandes brouillon", message: `${draftCount} commande(s) en attente`, action: "sale.action_orders" });
            try {
                const today = new Date().toISOString().split("T")[0];
                const overdue = await orm.searchCount("account.move", [["move_type", "=", "out_invoice"], ["payment_state", "!=", "paid"], ["invoice_date_due", "<", today]]);
                if (overdue > 0) insights.push({ id: "overdue_inv", type: "danger", title: "Factures en retard", message: `${overdue} facture(s) à échéance dépassée`, action: "account.action_out_invoice_tree" });
            } catch (_) {}
            if (insights.length === 0) insights.push({ id: "ok", type: "success", title: "Tout va bien", message: "Aucune alerte.", action: null });
        } catch (_) {}
        this.state.insights = insights;
    }

    /** Mes tâches (assignées à moi) */
    async loadTasks() {
        try {
            const uid = this.env.services.user?.userId;
            if (!uid) return;
            const records = await this.orm.searchRead(
                "project.task",
                [["user_ids", "in", [uid]]],
                ["name", "project_id", "date_deadline", "priority"],
                { limit: 8, order: "date_deadline asc, priority desc" }
            );
            this.state.tasks = records;
        } catch (_) {
            this.state.tasks = [];
        }
    }

    /** Actions à faire (commandes brouillon, factures, etc.) */
    async loadActionsDue() {
        const actions = [];
        try {
            const draftSo = await this.orm.searchRead("sale.order", [["state", "=", "draft"]], ["name", "partner_id", "amount_total"], { limit: 3 }).catch(() => []);
            draftSo.forEach((r) => actions.push({ id: `so-${r.id}`, type: "Commande brouillon", name: r.name, extra: r.partner_id?.[1], model: "sale.order", resId: r.id }));
            const today = new Date().toISOString().split("T")[0];
            const overdue = await this.orm.searchRead("account.move", [["move_type", "=", "out_invoice"], ["payment_state", "!=", "paid"], ["invoice_date_due", "<", today]], ["name", "partner_id", "amount_residual"], { limit: 3 }).catch(() => []);
            overdue.forEach((r) => actions.push({ id: `inv-${r.id}`, type: "Facture impayée", name: r.name, extra: r.partner_id?.[1], model: "account.move", resId: r.id }));
            this.state.actionsDue = actions;
        } catch (_) {
            this.state.actionsDue = [];
        }
    }

    /** Suggestions (leads à relancer, opportunités) */
    async loadSuggestions() {
        try {
            const leads = await this.orm.searchRead("crm.lead", [["type", "=", "opportunity"]], ["name", "partner_id", "expected_revenue", "date_deadline"], { limit: 5, order: "date_deadline asc" }).catch(() => []);
            this.state.suggestions = leads.map((r) => ({ id: r.id, name: r.name, partner: r.partner_id?.[1], revenue: r.expected_revenue, date: r.date_deadline, action: "crm.crm_lead_action_opportunities" }));
        } catch (_) {
            this.state.suggestions = [];
        }
    }

    /** Indicateurs de performance de l'utilisateur */
    async loadUserIndicators() {
        const indicators = [];
        try {
            const uid = this.env.services.user?.userId;
            const orm = this.orm;
            const myTasksTotal = await orm.searchCount("project.task", [["user_ids", "in", [uid]]]).catch(() => 0);
            const myTasksDone = await orm.searchCount("project.task", [["user_ids", "in", [uid]], ["stage_id.fold", "=", true]]).catch(() => 0);
            indicators.push({ id: "tasks", label: "Mes tâches actives", value: myTasksTotal, icon: "fa fa-tasks", action: "project.action_view_task" });
            indicators.push({ id: "done", label: "Tâches complétées", value: myTasksDone, icon: "fa fa-check-circle", action: "project.action_view_task" });
            const myLeads = await orm.searchCount("crm.lead", [["user_id", "=", uid]]).catch(() => 0);
            if (myLeads > 0) indicators.push({ id: "leads", label: "Mes opportunités", value: myLeads, icon: "fa fa-bullhorn", action: "crm.crm_lead_action_opportunities" });
            const mySales = await orm.searchCount("sale.order", [["user_id", "=", uid], ["state", "in", ["sale", "done"]]]).catch(() => 0);
            if (mySales > 0) indicators.push({ id: "sales", label: "Mes ventes", value: mySales, icon: "fa fa-shopping-cart", action: "sale.action_orders" });
            this.state.userIndicators = indicators;
        } catch (_) {
            this.state.userIndicators = [];
        }
    }

    /** Congés à valider (pour manager) */
    async loadLeaves() {
        try {
            const records = await this.orm.searchRead("hr.leave", [["state", "=", "confirm"]], ["name", "employee_id", "date_from", "date_to"], { limit: 5 }).catch(() => []);
            this.state.leaves = records.map((r) => ({ id: r.id, name: r.name, employee: r.employee_id?.[1], from: r.date_from, to: r.date_to, action: "hr_holidays.hr_leave_action_action_to_approve" }));
        } catch (_) {
            this.state.leaves = [];
        }
    }

    /** Réunions du jour */
    async loadMeetings() {
        try {
            const today = new Date().toISOString().split("T")[0];
            const records = await this.orm.searchRead("calendar.event", [["start", ">=", today + " 00:00:00"], ["start", "<=", today + " 23:59:59"]], ["name", "start", "partner_ids"], { limit: 5 }).catch(() => []);
            this.state.meetings = records.map((r) => ({ id: r.id, name: r.name, start: r.start, action: "calendar.action_calendar_event" }));
        } catch (_) {
            this.state.meetings = [];
        }
    }

    /** Activité récente globale */
    async loadGlobalActivity() {
        const activity = [];
        const models = [
            { model: "sale.order", nameField: "name", dateField: "date_order", label: "Commande" },
            { model: "crm.lead", nameField: "name", dateField: "create_date", label: "Lead" },
            { model: "project.task", nameField: "name", dateField: "write_date", label: "Tâche" },
        ];
        for (const { model, nameField, dateField, label } of models) {
            try {
                const records = await this.orm.searchRead(model, [], [nameField, dateField], { limit: 4, order: dateField + " desc" });
                records.forEach((r) => activity.push({ id: `${model}-${r.id}`, type: label, name: r[nameField] || r.display_name, date: r[dateField] }));
            } catch (_) {}
        }
        this.state.activity = activity.slice(0, 12).sort((a, b) => new Date(b.date) - new Date(a.date));
    }

    /**
     * Charge les KPIs (comptages) — modèles standards + CRM/Ventes/Projet si installés.
     * Ajoute actionXmlId pour rendre les KPIs cliquables.
     */
    async loadKpis() {
        const kpis = [];
        const candidates = [
            { model: "res.partner", label: "Contacts", icon: "fa fa-users", actionXmlId: "base.action_partner_form" },
            { model: "crm.lead", label: "Opportunités", icon: "fa fa-bullhorn", actionXmlId: "crm.crm_lead_action_opportunities" },
            { model: "sale.order", label: "Commandes", icon: "fa fa-shopping-cart", actionXmlId: "sale.action_orders" },
            { model: "project.project", label: "Projets", icon: "fa fa-project-diagram", actionXmlId: "project.open_view_project_all" },
            { model: "project.task", label: "Tâches", icon: "fa fa-tasks", actionXmlId: "project.action_view_task" },
            { model: "hr.employee", label: "Employés", icon: "fa fa-id-badge", actionXmlId: "hr.open_view_employee_list_my" },
            { model: "account.move", label: "Factures", icon: "fa fa-file-text-o", actionXmlId: "account.action_out_invoice_tree" },
        ];
        for (const { model, label, icon, actionXmlId } of candidates) {
            try {
                const count = await this.orm.searchCount(model, []);
                kpis.push({ id: model, label, value: count, icon, actionXmlId });
            } catch (_e) {
                // Module non installé ou pas de droit : on ignore
            }
        }
        this.state.kpis = kpis;
    }

    /**
     * Ouvre la liste Odoo correspondant à un KPI.
     */
    openKpiList(kpi) {
        if (kpi.actionXmlId) {
            // Utiliser l'xmlid directement (Odoo 18 le supporte)
            this.actionService.doAction(kpi.actionXmlId);
        } else {
            // Fallback : recherche générique par modèle
            this.actionService.doAction({
                type: "ir.actions.act_window",
                res_model: kpi.id,
                views: [[false, "list"], [false, "form"]],
                target: "current",
            });
        }
    }

    /**
     * Formate un montant en devise.
     */
    formatCurrency(amount) {
        if (typeof amount !== "number") return amount;
        return new Intl.NumberFormat("fr-FR", { style: "currency", currency: "XOF", minimumFractionDigits: 0 }).format(amount);
    }

    /**
     * Formate une date.
     */
    formatDate(dateStr) {
        if (!dateStr) return "";
        const date = new Date(dateStr);
        return date.toLocaleDateString("fr-FR", { day: "numeric", month: "short", year: "numeric" });
    }

    /**
     * Formate une date courte (jour/mois).
     */
    formatShortDate(dateStr) {
        if (!dateStr) return "";
        const date = new Date(dateStr);
        return date.toLocaleDateString("fr-FR", { day: "numeric", month: "short" });
    }

    openInsight(insight) {
        if (insight.action) this.actionService.doAction(insight.action);
    }

    openActionDue(item) {
        if (item.model && item.resId) this.actionService.doAction({ type: "ir.actions.act_window", res_model: item.model, res_id: item.resId, views: [[false, "form"]], target: "current" });
    }

    openTask(task) {
        this.actionService.doAction({ type: "ir.actions.act_window", res_model: "project.task", res_id: task.id, views: [[false, "form"]], target: "current" });
    }

    openSuggestion(s) {
        if (s.action) this.actionService.doAction(s.action);
    }

    openUserIndicator(ind) {
        if (ind.action) this.actionService.doAction(ind.action);
    }

    openLeave(l) {
        if (l.action) this.actionService.doAction(l.action);
    }

    openMeeting(m) {
        if (m.action) this.actionService.doAction({ type: "ir.actions.act_window", res_model: "calendar.event", res_id: m.id, views: [[false, "form"]], target: "current" });
    }
}

CoyaHomeDashboard.template = "coya_modern_navbar.CoyaHomeDashboard";

registry.category("actions").add("coya_home_dashboard", CoyaHomeDashboard);
