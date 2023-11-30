import { type Component as VueComponent } from "@vue/runtime-core";
import { type Router, type RouteRecordRaw } from "vue-router";

import { ComponentState } from "../../../data/stores/ComponentStore";
import { View } from "../View";

import Connecting from "./states/Connecting.vue";
import ConnectionError from "./states/ConnectionError.vue";
import ConnectionLost from "./states/ConnectionLost.vue";

/**
 * The main view enclosing/containing the entire component.
 */
export class MainView extends View {
    private readonly _appRoot: VueComponent;

    /**
     * @param router - The main Vue router.
     * @param appRoot - The root (main) application component.
     * @param routeOptions - Additional route options.
     * @param subViews - Optional sub-views.
     */
    public constructor(router: Router, appRoot: VueComponent, routeOptions?: RouteRecordRaw, subViews?: View[]) {
        super(router, "main", routeOptions, subViews);

        this._appRoot = appRoot;
    }

    protected defineRoute(): RouteRecordRaw {
        return {
            path: "/",
            component: () => import("./MainView.vue"),
            name: this._routeName
        };
    }

    /**
     * Get the Vue component for the specified global commponent state.
     *
     * @param state - The global component state.
     *
     * @throws Error - If the component state is unknown.
     */
    public getStateComponent(state: ComponentState): VueComponent {
        switch (state) {
            case ComponentState.Connecting:
                return Connecting;
            case ComponentState.ConnectionLost:
                return ConnectionLost;
            case ComponentState.ConnectionError:
                return ConnectionError;
            case ComponentState.Running:
                return this._appRoot;
        }
        throw new Error(`The component state '${state}' is unknown`);
    }
}
