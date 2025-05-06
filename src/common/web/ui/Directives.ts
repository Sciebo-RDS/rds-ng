/**
 * Custom Vue directives.
 */
export function useDirectives() {
    const vFocus = {
        mounted: (el: HTMLElement) => {
            setTimeout(() => {
                el.focus();
            }, 250);
        }
    };

    return {
        vFocus
    };
}
