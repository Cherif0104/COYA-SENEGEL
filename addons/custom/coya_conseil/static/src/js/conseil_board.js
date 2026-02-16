/** @odoo-module */

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";

export class ConseilBoard extends Component {
    setup() {
        this.menu = useService("menu");
        this.action = useService("action");
    }

    async openMenu(ev) {
        const menuId = ev.currentTarget.dataset.menu;
        if (menuId === "trinite") {
            await this.action.doAction("coya_trinite.action_coya_trinite_dashboard");
        } else if (menuId === "programme") {
            await this.action.doAction("coya_programme_budget.action_coya_programme");
        } else if (menuId === "juridique") {
            await this.action.doAction("coya_juridique.action_coya_juridique_risque");
        }
    }
}

ConseilBoard.template = "coya_conseil_board.ConseilBoard";

registry.category("actions").add("coya_conseil_board", ConseilBoard);
