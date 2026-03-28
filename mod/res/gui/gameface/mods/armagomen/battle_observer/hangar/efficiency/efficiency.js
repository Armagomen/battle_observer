import { MediaContext } from "coui://gui/gameface/mods/libs/media.js";
import { ModelObserver } from "coui://gui/gameface/mods/libs/model.js";

const media = MediaContext(false);
const model = ModelObserver("Observer_Efficiency_UI");

let effContainer;

function applyScale() {
    let scale = 1;

    const fightButton = document.querySelector('#fight-button');
    if (fightButton) {
        const style = window.getComputedStyle(fightButton);
        const transform = style.transform;

        if (transform && transform !== "none") {
            const match = transform.match(/scale\(([^)]+)\)/);
            if (match) {
                const parts = match[1].split(",");
                scale = parseFloat(parts[parts.length - 1]);
            } else if (transform.startsWith("matrix")) {
                const values = transform.match(/matrix\(([^)]+)\)/)[1].split(",");
                scale = parseFloat(values[3]);
            }
        }

        const rect = fightButton.getBoundingClientRect();
        const bottom = rect.bottom;

        const offset = Math.floor(10 * scale);
        const newTopPx = bottom + offset;

        effContainer.style.top = `${newTopPx}px`;
        effContainer.style.left = "50vw";
        effContainer.style.transform = `translateX(-50%) scale(${scale})`;
    }
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
        setTimeout(applyScale, 100);
    });
    media.subscribe();

    model.onUpdate(updateEfficiency);
    model.subscribe();

    setTimeout(applyScale, 100);

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