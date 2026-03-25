import { MediaContext } from "coui://gui/gameface/mods/libs/media.js";
import { ModelObserver } from "coui://gui/gameface/mods/libs/model.js";

const media = MediaContext(false);
const model = ModelObserver("Observer_DateTimes_UI");

let clockContainer;

function applyScale() {
    const baseWidth = 1920, baseHeight = 1080;
    const scaleX = media.width / baseWidth;
    const scaleY = media.height / baseHeight;
    const scale = Math.min(scaleX, scaleY, media.scale);

    clockContainer.style.top = "26vh";
    clockContainer.style.left = "4vw";
    clockContainer.style.transform = `translateY(-50%) scale(${scale})`;
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
        applyScale();
    });
    media.subscribe();

    model.onUpdate(updateClock);
    model.subscribe();

    applyScale();

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