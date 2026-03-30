import {MediaContext} from "coui://gui/gameface/mods/libs/media.js";
import {ModelObserver} from "coui://gui/gameface/mods/libs/model.js";
import {getScaleAndNewPosition, waitForElement, watchVisibilityBySelector} from "../../../utils.js";

const media = MediaContext(false);
const model = ModelObserver("Observer_Efficiency_UI");

function getEffContainer() {
    return document.querySelector(".bo_effContainer");
}

async function applyScale() {
    const eff = getEffContainer();
    if (!eff) return;

    const {scale, newTopPx} = await getScaleAndNewPosition("#fight-button", media);
    eff.style.top = `${newTopPx}px`;
    eff.style.transform = `translateX(-50%) scale(${scale})`;
}

function updateEfficiency() {
    const eff = getEffContainer();
    if (!eff) return;

    eff.innerHTML = model?.model?.effHtmlText ?? "";
}

engine.whenReady.then(async () => {
    const fightButton = await waitForElement("#fight-button");
    const headerSection = fightButton.parentNode;

    const eff = document.createElement("div");
    eff.setAttribute("data-bo", "true");
    eff.className = "bo_effContainer";
    eff.innerHTML = "";
    headerSection.appendChild(eff);

    media.onUpdate(applyScale);
    media.subscribe();

    model.onUpdate(updateEfficiency);
    model.subscribe();

    applyScale();

    watchVisibilityBySelector(eff, "[class*='UserProfile_']");
});
