
const OBSERVE_CHILD_LIST = {childList: true, subtree: true};

/**
 * Waits for an element matching selector to appear in the DOM.
 * Resolves with the element once found.
 *
 * @param {string} selector - CSS selector of the element to wait for.
 * @returns {Promise<HTMLElement>}
 */
function waitForElement(selector) {
    return new Promise(resolve => {
        const existing = document.querySelector(selector);
        if (existing) return resolve(existing);

        const observer = new MutationObserver(mutations => {
            if (mutations.length === 0) return;
            const el = document.querySelector(selector);
            if (el) {
                resolve(el);
                observer.disconnect();
            }
        });

        observer.observe(document.body, OBSERVE_CHILD_LIST);

    });
}


/**
 * Prints a flat list of all descendant elements of a given root
 * to the console, including their index, tag name, id, class names,
 * and key computed style properties (z-index, position, opacity, transform).
 * Useful for debugging and inspecting the DOM stacking context and layout.
 *
 * @param {HTMLElement} [root=document.body] - The root element to start from.
 * @returns {void} - Outputs element information to console.error.
 *
 * Example output:
 * 0: <div>#main.container [z-index:auto] [position:relative] [opacity:1]
 * 1: <span>.highlight [z-index:10] [position:absolute] [opacity:1] [transform:scale(1.2)]
 */
function printDOM(root = document.body) {
    for (const [i, child] of [...root.querySelectorAll("*")].entries()) {
        const style = window.getComputedStyle(child);

        console.error(
            `${i}: <${child.tagName.toLowerCase()}>` +
            (child.id ? `#${child.id}` : "") +
            (child.className ? `.${child.className}` : "") +
            ` [z-index:${style.zIndex}] [position:${style.position}] [opacity:${style.opacity}]` +
            (style.transform !== "none" ? ` [transform:${style.transform}]` : "")
        );
    }

    const elems = document.querySelectorAll('div[data-test-id]');

    elems.forEach(el => {
        console.error(el.dataset.testId);
    });

}


/**
 * Toggle container visibility explicitly using display property.
 *
 * @param {HTMLElement} container - The container to show/hide
 * @param {boolean} visible - true to show, false to hide
 * @param {string} displayType - Display mode when visible (default: "flex")
 */
function setVisibility(container, visible, displayType = "flex") {
    if (!container || !container.style) {
        const err = new Error("[BATTLE_OBSERVER] setVisibility: container is null or has no style");
        console.error(err.message, "node:", container?.nodeName, "\nstack:", err.stack);
        return;
    }
    const newType = visible ? displayType : "none";
    if (container.style.display !== newType) {
        container.style.display = newType;
    }
}


/**
 * Observe DOM mutations and toggle container visibility
 * depending on whether nodes matching selector are added or removed.
 *
 * @param {HTMLElement} container - The container to show/hide
 * @param {string} selector - CSS selector to check
 * @returns {MutationObserver} - The observer instance
 */
function watchVisibilityBySelector(container, selector) {
    // Initial state check
    setVisibility(container, Boolean(document.querySelector(selector)));

    const observer = new MutationObserver(mutations => {
        if (mutations.length === 0) return;
        setVisibility(container, Boolean(document.querySelector(selector)));
    });

    observer.observe(document.body, OBSERVE_CHILD_LIST);
    return observer;
}


/**
 * Calculate a UI scale factor and determine a new vertical position
 * relative to a target element in the DOM.
 *
 * Waits briefly to allow the DOM to update, computes the scale based on
 * media dimensions and a predefined baseline, then finds the element
 * matching the selector and calculates a new top offset in pixels.
 *
 * @async
 * @param {string} selector - CSS selector for the target element
 * @param {Object} media - Media object containing height and scale properties
 * @param {number} [timeout=200] - Delay in milliseconds before calculation
 * @returns {Promise<{scale: number, newTopPx: number}>} - Computed scale and new top position
 */
async function getScaleAndNewPosition(selector, media, timeout = 200) {
    await new Promise(resolve => setTimeout(resolve, timeout));

    const scale = Math.min(Math.sqrt(media.height / 1080), media.scale);
    const element = await waitForElement(selector);
    const offset = Math.floor(14 * scale);
    const newTopPx = element.getBoundingClientRect().bottom + offset;

    return {scale, newTopPx};
}


// Export public functions and constants
export {waitForElement, printDOM, setVisibility, watchVisibilityBySelector, getScaleAndNewPosition, OBSERVE_CHILD_LIST};

