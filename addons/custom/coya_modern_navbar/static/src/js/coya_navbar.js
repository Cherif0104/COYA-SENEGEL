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

    async loadAppsInSidebar() {
        const menuService = this.env.services.menu;
        const actionService = this.env.services.action;
        const navList = document.getElementById("coya-nav-apps");
        if (!navList) return;

        try {
            const menuItems = await menuService.load("root");
            const apps = this.extractApps(menuItems);

            navList.innerHTML = apps
                .map(
                    (app) => `
                    <li class="coya-nav-item">
                        <a href="#" class="coya-nav-link" data-action-id="${app.action?.id || ''}" data-menu-id="${app.id}">
                            <i class="${(app.icon || "fa fa-cube").split(",")[1] || "fa fa-cube"}" aria-hidden="true"></i>
                            <span class="coya-nav-text">${app.name}</span>
                        </a>
                    </li>
                `
                )
                .join("");

            // Gérer les clics
            navList.querySelectorAll(".coya-nav-link").forEach((link) => {
                link.addEventListener("click", (e) => {
                    e.preventDefault();
                    const actionId = link.dataset.actionId;
                    const menuId = link.dataset.menuId;
                    if (actionId) {
                        actionService.doAction(actionId);
                    } else if (menuId) {
                        menuService.selectMenu(menuId);
                    }
                    navList.querySelectorAll(".coya-nav-link").forEach((l) => l.classList.remove("active"));
                    link.classList.add("active");
                });
            });
        } catch (error) {
            console.error("Erreur chargement apps sidebar:", error);
        }
    },

    extractApps(menuItems) {
        const apps = [];
        const processMenu = (items) => {
            if (!items || !Array.isArray(items)) return;
            for (const item of items) {
                if (item.action && item.action.type === "ir.actions.act_window") {
                    apps.push({
                        id: item.id,
                        name: item.name,
                        icon: item.web_icon || "fa fa-cube",
                        action: item.action,
                        sequence: item.sequence || 9999,
                    });
                }
                if (item.childrenTree) {
                    processMenu(item.childrenTree);
                }
            }
        };
        processMenu(menuItems.childrenTree || []);
        return apps.sort((a, b) => a.sequence - b.sequence);
    },
});

/**
 * Client Action : Tableau de bord d'accueil COYA
 */
export class CoyaHomeDashboard extends Component {
    setup() {
        this.menuService = useService("menu");
        this.userService = useService("user");
        this.actionService = useService("action");
        this.state = useState({
            apps: [],
            loading: true,
        });

        onMounted(() => {
            this.loadApps();
        });
    }

    async loadApps() {
        try {
            const menuItems = await this.menuService.load("root");
            const apps = this.extractApps(menuItems);
            this.state.apps = apps;
            this.state.loading = false;
        } catch (error) {
            console.error("Erreur chargement apps:", error);
            this.state.loading = false;
        }
    }

    extractApps(menuItems) {
        const apps = [];
        const processMenu = (items) => {
            if (!items || !Array.isArray(items)) return;
            for (const item of items) {
                if (item.action && item.action.type === "ir.actions.act_window") {
                    apps.push({
                        id: item.id,
                        name: item.name,
                        icon: item.web_icon || "fa fa-cube",
                        action: item.action,
                        sequence: item.sequence || 9999,
                    });
                }
                if (item.childrenTree) {
                    processMenu(item.childrenTree);
                }
            }
        };
        processMenu(menuItems.childrenTree || []);
        return apps.sort((a, b) => a.sequence - b.sequence);
    }
}

CoyaHomeDashboard.template = "coya_modern_navbar.CoyaHomeDashboard";

registry.category("actions").add("coya_home_dashboard", CoyaHomeDashboard);
