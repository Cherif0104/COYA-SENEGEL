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
            <nav class="coya-sidebar-nav">
                <div class="coya-nav-section">
                    <div class="coya-nav-section-title">MENU</div>
                    <ul class="coya-nav-list" id="coya-nav-apps">
                        <!-- Apps injectées par JS -->
                    </ul>
                </div>
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
                    <a href="#" class="coya-leader-link" data-menu-xmlid="base.menu_administration" title="Paramètres">
                        <i class="fa fa-cog"></i> Paramètres
                    </a>
                    <a href="#" class="coya-leader-link" data-menu-xmlid="base.menu_help" title="Aide">
                        <i class="fa fa-question-circle"></i> Aide
                    </a>
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

    loadAppsInSidebar() {
        const menuService = this.env.services.menu;
        const actionService = this.env.services.action;
        const navList = document.getElementById("coya-nav-apps");
        if (!navList) return;

        try {
            // Applications racines uniquement (CRM, Ventes, Paramètres, etc.) — déjà filtrées par droits backend
            const apps = menuService.getApps();
            const sorted = [...apps].sort((a, b) => (a.sequence ?? 9999) - (b.sequence ?? 9999));

            navList.innerHTML = sorted
                .map(
                    (app) => {
                        const iconClass = (app.webIcon || "fa fa-cube").split(",")[1] || "fa fa-cube";
                        const actionId = app.actionID || "";
                        return `
                    <li class="coya-nav-item">
                        <a href="#" class="coya-nav-link" data-action-id="${actionId}" data-menu-id="${app.id}">
                            <i class="${iconClass}" aria-hidden="true"></i>
                            <span class="coya-nav-text">${app.name}</span>
                        </a>
                    </li>
                `;
                    }
                )
                .join("");

            navList.querySelectorAll(".coya-nav-link").forEach((link) => {
                link.addEventListener("click", (e) => {
                    e.preventDefault();
                    const actionId = link.dataset.actionId;
                    const menuId = link.dataset.menuId;
                    if (actionId) {
                        actionService.doAction(parseInt(actionId, 10));
                    } else if (menuId) {
                        menuService.selectMenu(parseInt(menuId, 10));
                    }
                    navList.querySelectorAll(".coya-nav-link").forEach((l) => l.classList.remove("active"));
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
            await Promise.all([this.loadKpis(), this.loadDomainPreviews(domains)]);
        } catch (error) {
            console.error("Erreur chargement dashboard:", error);
        } finally {
            this.state.loading = false;
        }
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
}

CoyaHomeDashboard.template = "coya_modern_navbar.CoyaHomeDashboard";

registry.category("actions").add("coya_home_dashboard", CoyaHomeDashboard);
