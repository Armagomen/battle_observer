import {MediaContext} from "coui://gui/gameface/mods/libs/media.js";
import {ModelObserver} from "coui://gui/gameface/mods/libs/model.js";
import {getScaleAndNewPosition, waitForElement, watchVisibilityBySelector} from "../../../utils.js";

const media = MediaContext(false);
const model = ModelObserver("Observer_DateTimes_UI");

const fight_button_selector = "#fight-button";
const user_profile_selector = "div[class*='UserProfile_']";

const container_style = "bo_clockContainer";


function getClockContainer() {
    return document.querySelector(`div.${container_style}`);
}


async function applyScale() {
    const clock = getClockContainer();
    if (!clock) return;

    const {scale, newTopPx} = await getScaleAndNewPosition(fight_button_selector, media);
    clock.style.top = `${newTopPx}px`;
    clock.style.transform = `scale(${scale})`;
}


function updateClock() {
    const clock = getClockContainer();
    if (!clock) return;

    clock.innerHTML = model?.model?.clock ?? "";
}


function createContainer(headerSection) {
    let container = getClockContainer();
    if (!container) {
        container = document.createElement("div");
        container.className = container_style;
        headerSection.appendChild(container);
        applyScale();
    }
    return container;
}


engine.whenReady.then(async () => {
    const fightButton = await waitForElement(fight_button_selector);
    if (!fightButton) return;
    watchVisibilityBySelector(createContainer(fightButton.parentNode), user_profile_selector);

    media.onUpdate(applyScale);
    media.subscribe();

    model.onUpdate(updateClock);
    model.subscribe();
});