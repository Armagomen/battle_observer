import {MediaContext} from "coui://gui/gameface/mods/libs/media.js";
import {ModelObserver} from "coui://gui/gameface/mods/libs/model.js";
import {getScaleAndNewPosition, waitForElement, watchVisibilityBySelector} from "../../../utils.js";

const media = MediaContext(false);
const model = ModelObserver("Observer_DateTimes_UI");

function getClockContainer() {
    return document.querySelector(".bo_clockContainer");
}

async function applyScale() {
    const clock = getClockContainer();
    if (!clock) return;

    const {scale, newTopPx} = await getScaleAndNewPosition("#fight-button", media);
    clock.style.top = `${newTopPx}px`;
    clock.style.transform = `scale(${scale})`;
}

function updateClock() {
    const clock = getClockContainer();
    if (!clock) return;

    clock.innerHTML = model?.model?.clock ?? "";
}

engine.whenReady.then(async () => {
    const fightButton = await waitForElement("#fight-button");
    const headerSection = fightButton.parentNode;

    const clock = document.createElement("div");
    clock.setAttribute("data-bo", "true");
    clock.className = "bo_clockContainer";
    clock.innerHTML = "";
    headerSection.appendChild(clock);

    media.onUpdate(applyScale);
    media.subscribe();

    model.onUpdate(updateClock);
    model.subscribe();

    applyScale();

    watchVisibilityBySelector(clock, "[class*='UserProfile_']");
});
