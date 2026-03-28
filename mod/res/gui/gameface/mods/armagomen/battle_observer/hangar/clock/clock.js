import { MediaContext } from "coui://gui/gameface/mods/libs/media.js";
import { ModelObserver } from "coui://gui/gameface/mods/libs/model.js";

const media = MediaContext(false);
const model = ModelObserver("Observer_DateTimes_UI");

let clockContainer;

function applyScale() {
    let scale = 1;

    const fightButton = document.querySelector("#fight-button");
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

        clockContainer.style.top = `${newTopPx}px`;
        clockContainer.style.left = "4vw";
        clockContainer.style.transform = `scale(${scale})`;
    }
}

function updateClock() {
    const fightButton = document.querySelector("#fight-button");
    if (!fightButton) {
        clockContainer.innerHTML = "";
    } else {
        clockContainer.innerHTML = model.model.clock || "";
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

    clockContainer = document.createElement("div");
    clockContainer.className = "bo_clockContainer";
    clockContainer.innerHTML = "";
    headerSection.appendChild(clockContainer);

    media.onUpdate(() => {
        updateClock();
        setTimeout(applyScale, 100);
    });
    media.subscribe();

    model.onUpdate(updateClock);
    model.subscribe();

    setTimeout(applyScale, 100);

    const observer = new MutationObserver(mutations => {
        for (const m of mutations) {
            const affected = [...m.addedNodes, ...m.removedNodes];
            if (affected.some(n => n.id === "fight-button" || n.querySelector?.("#fight-button"))) {
                updateClock();
            }
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });
});