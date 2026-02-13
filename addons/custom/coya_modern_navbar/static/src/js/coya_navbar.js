/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { NavBar } from "@web/webclient/navbar/navbar";
import { Component, onMounted, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

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
                        <a href="#" class="coya-nav-link" data-menu-xmlid="base.menu_administration">
                            <i class="fa fa-cog" aria-hidden="true"></i>
                            <span class="coya-nav-text">Paramètres</span>
                        </a>
                    </li>
                    <li class="coya-nav-item">
                        <a href="#" class="coya-nav-link" data-menu-xmlid="base.menu_help">
                            <i class="fa fa-question-circle" aria-hidden="true"></i>
                            <span class="coya-nav-text">Aide</span>
                        </a>
                    </li>
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

        // Ajuster le contenu principal
        const actionManager = document.querySelector(".o_action_manager");
        if (actionManager) {
            actionManager.classList.add("coya-main-content");
        }

        // Charger les apps dans la sidebar
        this.loadAppsInSidebar();
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

            this.bindFooterMenuLinks();
        } catch (error) {
            console.error("Erreur chargement apps sidebar:", error);
        }
    },

    bindFooterMenuLinks() {
        const menuService = this.env.services.menu;
        document.querySelectorAll(".coya-sidebar-footer .coya-nav-link[data-menu-xmlid]").forEach((link) => {
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
        this.state = useState({
            domains: [],
            loading: true,
        });

        onMounted(() => {
            this.loadDashboard();
        });
    }

    loadDashboard() {
        try {
            const root = this.menuService.getMenuAsTree("root");
            const domains = this.buildDomainsWithShortcuts(root);
            this.state.domains = domains;
            this.state.loading = false;
        } catch (error) {
            console.error("Erreur chargement dashboard:", error);
            this.state.loading = false;
        }
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
