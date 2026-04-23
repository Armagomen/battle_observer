import {ModelObserver} from "coui://gui/gameface/mods/libs/model.js";
import {OBSERVE_CHILD_LIST, setVisibility} from "../../../utils.js";

const model = ModelObserver("Observer_Header_UI");

const prem_selector = "div[data-test-id='premium']";
const prem_texts_selector = "[class*='Premiums_text']";
const wotPlus_selector = "div[data-test-id='wotPlus']";
const prem_shop_selector = "div[class*='Premiums_premiumShopImg']";
const format_texts_selector = "[class*='FormatText']";

const premium_style = "bo_premiumContainer";


function getContainers() {
    const premium = document.querySelector(`div.${premium_style}`);
    const premium_wg = document.querySelector(prem_selector);
    return {premium, premium_wg};
}


function updatePremium() {
    const {premium, premium_wg} = getContainers();
    if (!premium || !premium_wg || !premium._content) return;

    const timer = model?.model?.premium_timer ?? "";
    premium._content.textContent = timer;

    const visible = timer !== "";
    setVisibility(premium_wg.querySelector(prem_texts_selector), !visible);
    setVisibility(premium, visible);
}


function createContainer(premium_wg) {
    const premText = premium_wg.querySelector(prem_texts_selector);
    const formatText = premium_wg.querySelector(format_texts_selector);

    const premium = document.createElement("div");
    premium.classList.add(...(premText?.classList ?? []), premium_style);

    const content = document.createElement("span");
    content.classList.add(...(formatText?.classList ?? []), "bo_span");

    const wrapper = document.createElement("span");
    wrapper.appendChild(content);

    premium.appendChild(wrapper);
    premium._content = content;

    premium_wg.appendChild(premium);
    updatePremium();
}


function updateComponents() {
    const hide_shop = !model?.model?.hide_shop;
    const hide_wotPlus = !model?.model?.hide_wotPlus

    const shop_icon = document.querySelector(prem_shop_selector);
    const shop_container = shop_icon?.parentNode;
    if (shop_container && shop_container.previousElementSibling) {
        setVisibility(shop_container.previousElementSibling, hide_shop);
        setVisibility(shop_container, hide_shop);
    }
    const wotPlus = document.querySelector(wotPlus_selector);
    if (wotPlus && wotPlus.nextElementSibling) {
        setVisibility(wotPlus.nextElementSibling, hide_wotPlus);
        setVisibility(wotPlus, hide_wotPlus);
    }
}


engine.whenReady.then(() => {
    const observer = new MutationObserver(mutations => {
        if (mutations.length === 0) return;
        updateComponents();
        const {premium, premium_wg} = getContainers();
        if (!premium_wg) {
            return;
        }
        if (!premium) {
            createContainer(premium_wg);
        }
    });

    observer.observe(document.body, OBSERVE_CHILD_LIST);
    model.onUpdate(() => {
        updatePremium();
        updateComponents();
    });
    model.subscribe();
});
