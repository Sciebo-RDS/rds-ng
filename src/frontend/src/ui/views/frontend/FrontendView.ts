import { type Router, type RouteRecordRaw } from "vue-router";

import { NestedView } from "@common/ui/views/NestedView";

/**
 * The main view enclosing/containing the entire component.
 */
export class FrontendView extends NestedView {
    /**
     * @param router - The main Vue router.
     */
    public constructor(router: Router) {
        super(router, "frontend");
    }

    /**
     * Defines the route for this view.
     */
    protected defineRoute(): RouteRecordRaw {
        return {
            path: `${FrontendView.rootPath}/:project_id?`,
            component: () => import("./FrontendView.vue"),
            name: this._routeName
        };
    }

    /**
     * The root path of the frontend.
     */
    public static get rootPath(): string {
        return "project";
    }
}
