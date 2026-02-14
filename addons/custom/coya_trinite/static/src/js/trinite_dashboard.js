/** @odoo-module **/

import { Component, onMounted, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { user } from "@web/core/user";

/**
 * Dashboard Trinité : 3 piliers (Ndiguel, Barké, Yar), seuil 30 %.
 */
export class CoyaTriniteDashboard extends Component {
    setup() {
        this.actionService = useService("action");
        this.orm = useService("orm");
        this.state = useState({
            score: null,
            alertes: [],
            loading: true,
        });

        onMounted(() => {
            this.loadDashboard();
        });
    }

    get pilierData() {
        const s = this.state.score || {};
        return [
            {
                id: "ndiguel",
                label: "Ndiguel (Productivité)",
                value: s.score_ndiguel ?? 0,
                desc: "Discipline, respect des plannings",
            },
            {
                id: "barke",
                label: "Barké (Profitabilité)",
                value: s.score_barke ?? 0,
                desc: "Impact, résultats",
            },
            {
                id: "yar",
                label: "Yar (Professionnalisme)",
                value: s.score_yar ?? 0,
                desc: "Éthique, qualité",
            },
        ];
    }

    async loadDashboard() {
        try {
            await Promise.all([this.loadScore(), this.loadAlertes()]);
        } catch (error) {
            console.error("Erreur chargement dashboard Trinité:", error);
        } finally {
            this.state.loading = false;
        }
    }

    async loadScore() {
        try {
            const uid = user.userId;
            const [emp] = await this.orm.searchRead(
                "hr.employee",
                [["user_id", "=", uid]],
                ["id"],
                { limit: 1 }
            ).catch(() => []);
            if (emp) {
                const today = new Date().toISOString().split("T")[0];
                const [latest] = await this.orm.searchRead(
                    "coya.trinite.score",
                    [["employee_id", "=", emp.id], ["periode_end", ">=", today]],
                    ["score_ndiguel", "score_barke", "score_yar"],
                    { limit: 1, order: "periode_end desc" }
                ).catch(() => []);
                if (latest) this.state.score = latest;
            }
            if (!this.state.score) {
                this.state.score = { score_ndiguel: 0, score_barke: 0, score_yar: 0 };
            }
        } catch (_) {
            this.state.score = { score_ndiguel: 0, score_barke: 0, score_yar: 0 };
        }
    }

    async loadAlertes() {
        try {
            const records = await this.orm.searchRead(
                "coya.trinite.alerte",
                [["state", "=", "open"]],
                ["employee_id", "pilier", "score", "seuil"],
                { limit: 10 }
            );
            const pilierLabels = {
                ndiguel: "Ndiguel (Productivité)",
                barke: "Barké (Profitabilité)",
                yar: "Yar (Professionnalisme)",
            };
            this.state.alertes = records.map((r) => ({
                id: r.id,
                employee: r.employee_id?.[1] || "",
                pilier: pilierLabels[r.pilier] || r.pilier,
                score: r.score,
                seuil: r.seuil,
            }));
        } catch (_) {
            this.state.alertes = [];
        }
    }

    openScores() {
        this.actionService.doAction("coya_trinite.action_coya_trinite_score");
    }

    openAlertes() {
        this.actionService.doAction("coya_trinite.action_coya_trinite_alerte");
    }

    openPlans() {
        this.actionService.doAction("coya_trinite.action_coya_trinite_plan");
    }

    openAlerte(a) {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            res_model: "coya.trinite.alerte",
            res_id: a.id,
            views: [[false, "form"]],
            target: "current",
        });
    }
}

CoyaTriniteDashboard.template = "coya_trinite.CoyaTriniteDashboard";

registry.category("actions").add("coya_trinite_dashboard", CoyaTriniteDashboard);
