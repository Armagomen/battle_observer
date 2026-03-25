import { MediaContext } from "coui://gui/gameface/mods/libs/media.js";
import { ModelObserver } from "coui://gui/gameface/mods/libs/model.js";

const media = MediaContext(false);
const model = ModelObserver("Observer_Efficiency_UI");

let effContainer;

function applyScale() {
    const baseWidth = 1920, baseHeight = 1080;
    const scaleX = media.width / baseWidth;
    const scaleY = media.height / baseHeight;
    const scale = Math.min(scaleX, scaleY, media.scale);

    effContainer.style.top = "63vh";
    effContainer.style.left = "50vw";
    effContainer.style.transform = `translate(-50%, -50%) scale(${scale})`;
}

function updateEfficiency() {
    const fightButton = document.querySelector("#fight-button");
    if (!fightButton) {
        effContainer.innerHTML = "";
    } else {
       effContainer.innerHTML = model.model.effHtmlText || "";
    }
}

function waitForElement(selector, interval = 100) {
    return new Promise(resolve => {
        const el = document.querySelector(selector);
        if (el) {
            resolve(el);
            return;
        }
        const timer = setInterval(() => {
            const el = document.querySelector(selector);
            if (el) {
                clearInterval(timer);
                resolve(el);
            }
        }, interval);
    });
}

engine.whenReady.then(async () => {
    const fightButton = await waitForElement("#fight-button");
    const headerSection = fightButton.parentNode;

    effContainer = document.createElement("div");
    effContainer.className = "bo_effContainer";
    effContainer.innerHTML = "";
    headerSection.appendChild(effContainer);

    media.onUpdate(() => {
        updateEfficiency();
        applyScale();
    });
    media.subscribe();

    model.onUpdate(updateEfficiency);
    model.subscribe();

    applyScale();

    const observer = new MutationObserver(mutations => {
        for (const m of mutations) {
            const affected = [...m.addedNodes, ...m.removedNodes];
            if (affected.some(n => n.id === "fight-button" || n.querySelector?.("#fight-button"))) {
                updateEfficiency();
            }
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });
});