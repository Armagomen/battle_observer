import { MediaContext } from "coui://gui/gameface/mods/libs/media.js";
import { ModelObserver } from "coui://gui/gameface/mods/libs/model.js";
import { waitForElement, watchVisibilityBySelector, getScaleAndNewPosition } from "coui://gui/gameface/mods/armagomen/utils.js";

const media = MediaContext(false);
const model = ModelObserver("Observer_Efficiency_UI");

let effContainer;

async function applyScale() {
    const { scale, newTopPx } = await getScaleAndNewPosition("#fight-button", media);

    effContainer.style.top = `${newTopPx}px`;
    effContainer.style.transform = `translateX(-50%) scale(${scale})`;
}

function updateEfficiency() {
    effContainer.innerHTML = model.model.effHtmlText;
}

engine.whenReady.then(async () => {
    const fightButton = await waitForElement("#fight-button");
    const headerSection = fightButton.parentNode;

    effContainer = document.createElement("div");
    effContainer.className = "bo_effContainer";
    effContainer.innerHTML = "";
    headerSection.appendChild(effContainer);

    media.onUpdate(applyScale);
    media.subscribe();

    model.onUpdate(updateEfficiency);
    model.subscribe();

    applyScale();

    const observer = watchVisibilityBySelector(effContainer, "[class*='UserProfile_']");
});