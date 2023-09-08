import { type RouteRecordRaw } from "vue-router";

import { type ViewActivation, View } from "../View";

/**
 * The connection error view.
 */
export class ConnectionErrorView extends View {
    public constructor() {
        super("connection-error");
    }

    /**
     * Defines the route for this view.
     */
    public route(): RouteRecordRaw {
        return {
            path: "/connection-error",
            component: () => import("./ConnectionErrorView.vue"),
            name: this._routeName,
        };
    }

    /**
     * Navigates to this view.
     *
     * @param error - The connection error.
     * @param replace - Whether to replace the current browsing history entry.
     *
     * @returns - A promise that can be used to react to page load events.
     */
    public activate(error: string, replace: boolean = false): ViewActivation {
        return this.navigateTo(replace, { error: error });
    }
}
