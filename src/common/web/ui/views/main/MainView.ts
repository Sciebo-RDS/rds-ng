import { type Component as VueComponent } from "@vue/runtime-core";
import { type Router, type RouteRecordRaw } from "vue-router";
import { ComponentState } from "../../../stores/ComponentStore";

import { View } from "../View";

import ConnectionError from "./states/ConnectionError.vue";
import ConnectionLost from "./states/ConnectionLost.vue";
import Initializing from "./states/Initializing.vue";

/**
 * The main view enclosing/containing the entire component.
 */
export class MainView extends View {
    private readonly _appRoot: VueComponent;

    /**
     * @param router - The main Vue router.
     * @param appRoot - The root (main) application component.
     */
    public constructor(router: Router, appRoot: VueComponent) {
        super(router, "main");

        this._appRoot = appRoot;
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
     * Get the Vue component for the specified global commponent state.
     *
     * @param state - The global component state.
     *
     * @throws Error - If the component state is unknown.
     */
    public getStateComponent(state: ComponentState): VueComponent {
        switch (state) {
            case ComponentState.Initializing:
                return Initializing;
            case ComponentState.Running:
                return this._appRoot;
            case ComponentState.ConnectionLost:
                return ConnectionLost;
            case ComponentState.ConnectionError:
                return ConnectionError;
        }
        throw new Error(`The component state '${state}' is unknown`);
    }
}
