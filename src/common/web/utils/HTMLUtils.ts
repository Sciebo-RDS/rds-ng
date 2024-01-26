/**
 * Scrolls an HTML element into view and focusses it.
 *
 * @param selector - The selector for the element.
 * @param autoFocus - Whether to set the focus to this element.
 */
export function scrollElementIntoView(selector: string, autoFocus: boolean = true): void {
    const el = document.querySelector(selector) as HTMLInputElement;
    el?.scrollIntoView({ block: "center", behavior: "smooth" });

    if (autoFocus) {
        el?.focus();
    }
}
