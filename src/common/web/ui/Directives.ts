/**
 * Custom Vue directives.
 */
export function useDirectives() {
    const vFocus = {
        mounted: (el: HTMLElement) => el.focus()
    };

    return {
        vFocus
    };
}
