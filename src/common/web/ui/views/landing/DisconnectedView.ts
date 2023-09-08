import { type RouteRecordRaw } from "vue-router";

import { type ViewActivation, View } from "../View";

/**
 * The disconnection view.
 */
export class DisconnectedView extends View {
    public constructor() {
        super("disconnected");
    }

    /**
     * Defines the route for this view.
     */
    public route(): RouteRecordRaw {
        return {
            path: "/disconnected",
            component: () => import("./DisconnectedView.vue"),
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
