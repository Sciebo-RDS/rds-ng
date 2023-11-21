/**
 * Custom Vue directives.
 */
export function useDirectives() {
    const vFocus = {
        mounted: (el) => el.focus()
    };

    return {
        vFocus
    };
}
