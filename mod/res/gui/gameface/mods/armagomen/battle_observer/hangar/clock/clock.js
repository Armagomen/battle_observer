import { MediaContext } from "coui://gui/gameface/mods/libs/media.js";
import { ModelObserver } from "coui://gui/gameface/mods/libs/model.js";
import { waitForElement, watchVisibilityBySelector, getScaleAndNewPosition } from "coui://gui/gameface/mods/armagomen/utils.js";

const media = MediaContext(false);
const model = ModelObserver("Observer_DateTimes_UI");

let clockContainer;

async function applyScale() {
    const { scale, newTopPx } = await getScaleAndNewPosition("#fight-button", media);

    clockContainer.style.top = `${newTopPx}px`;
    clockContainer.style.transform = `scale(${scale})`;
}

function updateClock() {
    clockContainer.innerHTML = model.model.clock;
}

engine.whenReady.then(async () => {
    const fightButton = await waitForElement("#fight-button");
    const headerSection = fightButton.parentNode;

    clockContainer = document.createElement("div");
    clockContainer.className = "bo_clockContainer";
    clockContainer.innerHTML = "";
    headerSection.appendChild(clockContainer);

    media.onUpdate(applyScale);
    media.subscribe();

    model.onUpdate(updateClock);
    model.subscribe();

    applyScale();

    const observer = watchVisibilityBySelector(clockContainer, "[class*='UserProfile_']");
});