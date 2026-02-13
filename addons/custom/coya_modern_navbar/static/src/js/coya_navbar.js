/** @odoo-module **/

import { Component, onMounted, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

/**
 * Client Action : Tableau de bord d'accueil COYA
 * Affiche toutes les applications accessibles + vue 360° selon habilitations
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
            this.initSidebar();
        });
    }

    async loadApps() {
        try {
            // Charger toutes les applications accessibles depuis le menu
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

    initSidebar() {
        // Injecter les apps dans la sidebar après un court délai pour que le DOM soit prêt
        setTimeout(() => {
            const navList = document.getElementById("coya-nav-apps");
            if (!navList) return;

            // Charger les apps depuis le menu Odoo
            this.menuService.load("root").then((menuItems) => {
                const apps = this.extractApps(menuItems);
                navList.innerHTML = apps
                    .map(
                        (app) => `
                        <li class="coya-nav-item">
                            <a href="#" class="coya-nav-link" data-action-id="${app.action.id}" data-menu-id="${app.id}">
                                <i class="${app.icon.split(',')[1] || 'fa fa-cube'}" aria-hidden="true"></i>
                                <span class="coya-nav-text">${app.name}</span>
                            </a>
                        </li>
                    `
                    )
                    .join("");

                // Gérer les clics sur les liens
                navList.querySelectorAll(".coya-nav-link").forEach((link) => {
                    link.addEventListener("click", (e) => {
                        e.preventDefault();
                        const actionId = link.dataset.actionId;
                        const menuId = link.dataset.menuId;
                        if (actionId) {
                            this.actionService.doAction(actionId);
                        } else if (menuId) {
                            this.menuService.selectMenu(menuId);
                        }
                        // Marquer comme actif
                        navList.querySelectorAll(".coya-nav-link").forEach((l) => l.classList.remove("active"));
                        link.classList.add("active");
                    });
                });
            });
        }, 500);

        // Mettre à jour le nom utilisateur
        setTimeout(() => {
            const userNameEl = document.getElementById("coya-user-name");
            if (userNameEl && this.userService.name) {
                userNameEl.textContent = this.userService.name;
            }
        }, 500);
    }
}

CoyaHomeDashboard.template = "coya_modern_navbar.CoyaHomeDashboard";

registry.category("actions").add("coya_home_dashboard", CoyaHomeDashboard);

/**
 * Initialisation de la sidebar au chargement de la page
 */
document.addEventListener("DOMContentLoaded", () => {
    // Gérer le survol de la sidebar (déjà géré par CSS, mais on peut ajouter des effets JS si besoin)
    const sidebar = document.getElementById("coya-sidebar");
    if (sidebar) {
        // Ajouter des animations ou interactions supplémentaires si nécessaire
    }
});
