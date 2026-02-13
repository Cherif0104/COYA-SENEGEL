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
            <div class="coya-sidebar-footer">
                <ul class="coya-nav-list">
                    <li class="coya-nav-item">
                        <a href="/web/session/logout" class="coya-nav-link">
                            <i class="fa fa-sign-out" aria-hidden="true"></i>
                            <span class="coya-nav-text">Déconnexion</span>
                        </a>
                    </li>
                </ul>
            </div>
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

        // Date/heure
        const updateDateTime = () => {
            const el = document.getElementById("coya-leader-datetime");
            if (el) {
                const now = new Date();
                el.textContent = now.toLocaleDateString("fr-FR", { weekday: "short", day: "numeric", month: "short", year: "numeric" }) + " — " + now.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" });
            }
        };
        updateDateTime();
        setInterval(updateDateTime, 60000);

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
        if (n.includes("accueil") || n.includes("home") || n.includes("discussion") || n.includes("discuss") || n.includes("calendrier") || n.includes("calendar") || n.includes("to-do") || n.includes("todo") || n.includes("tâches")) return "Core";
        if (n.includes("crm") || n.includes("ventes") || n.includes("sale") || n.includes("facturation") || n.includes("invoic") || n.includes("projet") || n.includes("project") || n.includes("feuille") || n.includes("timesheet")) return "Business";
        if (n.includes("achat") || n.includes("purchase") || n.includes("inventaire") || n.includes("stock") || n.includes("dépense") || n.includes("expense")) return "Opérations";
        if (n.includes("employé") || n.includes("employee") || n.includes("présence") || n.includes("attendance") || n.includes("recrutement") || n.includes("recruit") || n.includes("congé") || n.includes("leave") || n.includes("déjeuner") || n.includes("lunch") || n.includes("hr ") || n === "hr") return "RH";
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

            const sectionOrder = ["Core", "Business", "Opérations", "RH", "Marketing", "Système"];
            const sectionLabels = { Core: "Principal", Business: "Business", Opérations: "Opérations", RH: "RH", Marketing: "Marketing", Système: "Système" };
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
            domains: [],
            kpis: [],
            insights: [],
            activity: [],
            loading: true,
        });

        onMounted(() => {
            this.loadDashboard();
        });
    }

    async loadDashboard() {
        try {
            const root = this.menuService.getMenuAsTree("root");
            const domains = this.buildDomainsWithShortcuts(root);
            this.state.domains = domains;
            await Promise.all([
                this.loadKpis(),
                this.loadDomainPreviews(domains),
                this.loadInsights(),
                this.loadGlobalActivity(),
            ]);
        } catch (error) {
            console.error("Erreur chargement dashboard:", error);
        } finally {
            this.state.loading = false;
        }
    }

    /** Bloc 3 – Insights (alertes métier) */
    async loadInsights() {
        const insights = [];
        try {
            const orm = this.orm;
            const draftCount = await orm.searchCount("sale.order", [["state", "=", "draft"]]).catch(() => 0);
            if (draftCount > 0) {
                insights.push({ id: "draft_so", type: "warning", title: "Commandes brouillon", message: `${draftCount} commande(s) en attente`, action: "sale.action_orders" });
            }
            try {
                const today = new Date().toISOString().split("T")[0];
                const overdue = await orm.searchCount("account.move", [["move_type", "=", "out_invoice"], ["payment_state", "!=", "paid"], ["invoice_date_due", "<", today]]);
                if (overdue > 0) insights.push({ id: "overdue_inv", type: "danger", title: "Factures en retard", message: `${overdue} facture(s) à échéance dépassée`, action: "account.action_out_invoice_tree" });
            } catch (_) {}
            if (insights.length === 0) insights.push({ id: "ok", type: "success", title: "Tout va bien", message: "Aucune alerte pour le moment.", action: null });
        } catch (_) {}
        this.state.insights = insights;
    }

    /** Bloc 4 – Activité globale (dernières actions) */
    async loadGlobalActivity() {
        const activity = [];
        const models = [
            { model: "sale.order", nameField: "name", dateField: "date_order", label: "Commande" },
            { model: "crm.lead", nameField: "name", dateField: "create_date", label: "Lead" },
            { model: "project.task", nameField: "name", dateField: "write_date", label: "Tâche" },
        ];
        for (const { model, nameField, dateField, label } of models) {
            try {
                const records = await this.orm.searchRead(model, [], [nameField, dateField], { limit: 3, order: dateField + " desc" });
                records.forEach((r) => activity.push({ id: `${model}-${r.id}`, type: label, name: r[nameField] || r.display_name, date: r[dateField] }));
            } catch (_) {}
        }
        this.state.activity = activity.slice(0, 10).sort((a, b) => new Date(b.date) - new Date(a.date));
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
     * Charge les aperçus (dernières activités) par domaine.
     */
    async loadDomainPreviews(domains) {
        const domainModelMap = {
            "CRM": { model: "crm.lead", fields: ["name", "partner_id", "stage_id", "date_deadline"], limit: 5 },
            "Ventes": { model: "sale.order", fields: ["name", "partner_id", "amount_total", "state", "date_order"], limit: 5 },
            "Projets": { model: "project.task", fields: ["name", "project_id", "stage_id", "date_deadline"], limit: 5 },
            "Contacts": { model: "res.partner", fields: ["name", "email", "phone", "category_id"], limit: 5 },
        };
        for (const domain of domains) {
            const config = domainModelMap[domain.name];
            if (!config) continue;
            try {
                const records = await this.orm.searchRead(
                    config.model,
                    [],
                    config.fields,
                    { limit: config.limit, order: "write_date desc" }
                );
                domain.preview = { model: config.model, records, fields: config.fields };
                // Charger les données pour les graphiques (7 derniers jours)
                await this.loadDomainChart(domain, config.model);
            } catch (_e) {
                // Module non installé ou pas de droit : on ignore
            }
        }
    }

    /**
     * Charge les données pour les graphiques par domaine (7 derniers jours).
     */
    async loadDomainChart(domain, model) {
        try {
            const today = new Date();
            const sevenDaysAgo = new Date(today);
            sevenDaysAgo.setDate(today.getDate() - 7);
            const dateField = model === "sale.order" ? "date_order" : model === "crm.lead" ? "create_date" : "create_date";
            const records = await this.orm.searchRead(
                model,
                [[dateField, ">=", sevenDaysAgo.toISOString().split("T")[0]]],
                [dateField],
                { order: dateField + " asc" }
            );
            // Grouper par jour
            const dailyCounts = {};
            records.forEach((r) => {
                const date = r[dateField] ? r[dateField].split("T")[0] : null;
                if (date) {
                    dailyCounts[date] = (dailyCounts[date] || 0) + 1;
                }
            });
            // Créer un tableau pour les 7 derniers jours
            const chartData = [];
            for (let i = 6; i >= 0; i--) {
                const date = new Date(today);
                date.setDate(today.getDate() - i);
                const dateStr = date.toISOString().split("T")[0];
                chartData.push({ date: dateStr, count: dailyCounts[dateStr] || 0 });
            }
            if (domain.preview) {
                domain.preview.chartData = chartData;
            } else {
                domain.preview = { chartData };
            }
        } catch (_e) {
            // Ignorer les erreurs
        }
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

    /**
     * Construit les domaines (apps racines) avec raccourcis (app + enfants directs avec action).
     * Prêt pour widgets KPI/graphiques par domaine (à brancher sur vues/rapports Odoo).
     */
    buildDomainsWithShortcuts(menuNode) {
        const items = menuNode.childrenTree || [];
        return items
            .map((app) => {
                const shortcuts = [];
                if (app.actionID) {
                    shortcuts.push({ id: app.id, name: app.name, actionId: app.actionID });
                }
                (app.childrenTree || []).forEach((child) => {
                    if (child.actionID) {
                        shortcuts.push({
                            id: child.id,
                            name: child.name,
                            actionId: child.actionID,
                        });
                    }
                });
                return {
                    id: app.id,
                    name: app.name,
                    icon: app.webIcon || "fa fa-cube",
                    actionId: app.actionID,
                    sequence: app.sequence ?? 9999,
                    shortcuts,
                };
            })
            .filter((d) => d.shortcuts.length > 0)
            .sort((a, b) => a.sequence - b.sequence);
    }

    /** Ouvre l'action associée à un insight (Bloc 3) */
    openInsight(insight) {
        if (insight.action) this.actionService.doAction(insight.action);
    }
}

CoyaHomeDashboard.template = "coya_modern_navbar.CoyaHomeDashboard";

registry.category("actions").add("coya_home_dashboard", CoyaHomeDashboard);
