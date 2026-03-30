import {ModelObserver} from "coui://gui/gameface/mods/libs/model.js";
import {setVisibility} from "../../../utils.js";

const model = ModelObserver("Observer_Header_UI");

let observer
const observe_options = {childList: true, subtree: true};

function getContainers() {
    const premium = document.querySelector("div.bo_premiumContainer");
    const premium_wg = document.querySelector('div[data-test-id="premium"]');
    return {premium, premium_wg};
}

function updatePremium() {
    observer.disconnect();
    const {premium, premium_wg} = getContainers();
    if (!premium || !premium_wg || !premium._content) return;
    const timer = model?.model?.premium_timer ?? "";
    premium._content.textContent = timer;
    const visible = timer === "";
    setVisibility(premium_wg.querySelector("[class*='Premiums_text']"), visible);
    setVisibility(premium, !visible);
    observer.observe(document.body, observe_options);
}

function createContainer(premium_wg) {
    const premText = premium_wg.querySelector("[class*='Premiums_text']");
    const premium = document.createElement("div");
    premium.classList.add(...premText.classList, "bo_premiumContainer");
    const formatText = premium_wg.querySelector("[class*='FormatText']");
    const wrapper = document.createElement('span');
    const content = document.createElement('span');
    content.setAttribute("data-bo", "true");
    content.classList.add(...formatText.classList, "bo_span");
    wrapper.appendChild(content);
    premium.appendChild(wrapper);
    premium._content = content;
    premium_wg.insertBefore(premium, premText.nextElementSibling);
    return premium;
}

function hideComponents() {
    observer.disconnect();
    const hide_shop = !model?.model?.hide_shop;
    const hide_wotPlus = !model?.model?.hide_wotPlus

    const shop_icon = document.querySelector("[class*='Premiums_premiumShopImg']");
    const shop_container = shop_icon?.parentNode;
    if (shop_container && shop_container.previousElementSibling) {
        setVisibility(shop_container.previousElementSibling, hide_shop);
        setVisibility(shop_container, hide_shop);
    }
    const wotPlus = document.querySelector('div[data-test-id="wotPlus"]');
    if (wotPlus && wotPlus.nextElementSibling) {
        setVisibility(wotPlus.nextElementSibling, hide_wotPlus);
        setVisibility(wotPlus, hide_wotPlus);
    }
    observer.observe(document.body, observe_options);
}

engine.whenReady.then(() => {
    observer = new MutationObserver(mutations => {
        for (const mutation of mutations) {
            if (mutation.target.hasAttribute("data-bo")) continue;
            hideComponents();
            const {premium, premium_wg} = getContainers();
            if (!premium_wg) {
                return;
            }
            if (!premium) {
                createContainer(premium_wg);
                updatePremium();
            }
        }
    });

    observer.observe(document.body, observe_options);
    model.onUpdate(() => {
        updatePremium();
        hideComponents();
    });
    model.subscribe();
});
