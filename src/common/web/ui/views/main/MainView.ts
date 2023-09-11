import { type RouteRecordRaw } from "vue-router";

import { type ViewActivation, RoutedView } from "../RoutedView";

/**
 * The main view enclosing/containing the entire component.
 */
export class MainView extends RoutedView {
    public constructor() {
        super("main");
    }

    /**
     * Defines the route for this view.
     */
    public route(): RouteRecordRaw {
        return {
            path: "/",
            component: () => import("./MainView.vue"),
            name: this._routeName,
        };
    }

    /**
     * Navigates to this view.
     *
     * @param replace - Whether to replace the current browsing history entry.
     *
     * @returns - A promise that can be used to react to page load events.
     */
    public activate(replace: boolean = false): ViewActivation {
        return this.navigateTo(replace);
    }
}
