import {MediaContext} from "coui://gui/gameface/mods/libs/media.js";
import {ModelObserver} from "coui://gui/gameface/mods/libs/model.js";
import {getScaleAndNewPosition, waitForElement, watchVisibilityBySelector} from "../../../utils.js";

const media = MediaContext(false);
const model = ModelObserver("Observer_Efficiency_UI");

const fight_button_selector = "#fight-button";
const user_profile_selector = "div[class*='UserProfile_']";

const container_style = "bo_effContainer";


function getEffContainer() {
    return document.querySelector(`div.${container_style}`);
}


async function applyScale() {
    const eff = getEffContainer();
    if (!eff) return;

    const {scale, newTopPx} = await getScaleAndNewPosition(fight_button_selector, media);
    eff.style.top = `${newTopPx}px`;
    eff.style.transform = `translateX(-50%) scale(${scale})`;
}


function updateEfficiency() {
    const eff = getEffContainer();
    if (!eff) return;

    eff.innerHTML = model?.model?.effHtmlText ?? "";
}


function createContainer(headerSection) {
    let container = getEffContainer();
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

    model.onUpdate(updateEfficiency);
    model.subscribe();
});
