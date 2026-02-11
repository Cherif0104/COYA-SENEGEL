/** COYA.PRO – Overlay de chargement moderne (charte SENEGEL) */
(function () {
    "use strict";

    const OVERLAY_ID = "coya-splash-overlay";
    const MAX_WAIT_MS = 3200;
    const POLL_MS = 150;

    function createOverlay() {
        if (document.getElementById(OVERLAY_ID)) return;
        const div = document.createElement("div");
        div.id = OVERLAY_ID;
        div.className = "coya-splash-overlay";
        div.setAttribute("aria-hidden", "true");
        div.innerHTML = [
            '<div class="coya-splash-backdrop"></div>',
            '<div class="coya-splash-content">',
            '  <div class="coya-splash-logo-wrap">',
            '    <img src="/sunugest_branding/static/img/logo_senegel.png" alt="SENEGEL" class="coya-splash-logo"/>',
            '  </div>',
            '  <p class="coya-splash-title">COYA.PRO</p>',
            '  <p class="coya-splash-tagline">CITOYENNETÉ, TRANSPARENCE, COMPÉTENCES</p>',
            '  <div class="coya-splash-spinner"></div>',
            '</div>',
        ].join("");
        document.body.appendChild(div);
    }

    function removeOverlay() {
        const el = document.getElementById(OVERLAY_ID);
        if (!el) return;
        el.classList.add("coya-splash-out");
        setTimeout(function () {
            if (el.parentNode) el.parentNode.removeChild(el);
        }, 400);
    }

    function isAppReady() {
        var client = document.querySelector(".o_web_client");
        if (!client) return false;
        var actionManager = client.querySelector(".o_action_manager");
        if (actionManager && actionManager.children && actionManager.children.length > 0) return true;
        return false;
    }

    function startPolling() {
        var deadline = Date.now() + MAX_WAIT_MS;
        var t = setInterval(function () {
            if (isAppReady() || Date.now() >= deadline) {
                clearInterval(t);
                removeOverlay();
            }
        }, POLL_MS);
    }

    if (document.body) {
        createOverlay();
        startPolling();
    } else {
        document.addEventListener("DOMContentLoaded", function () {
            createOverlay();
            startPolling();
        });
    }
})();
