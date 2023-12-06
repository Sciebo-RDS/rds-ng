import { type Router } from "vue-router";

import { View } from "./View";

/**
 * A specialized nested view.
 */
export abstract class NestedView extends View {
    protected mountRoute(router: Router): void {
        // A nested view is never mounted directly in the router.
    }
}
