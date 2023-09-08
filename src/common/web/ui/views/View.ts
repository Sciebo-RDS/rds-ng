import { type LocationQueryRaw, type NavigationFailure, type RouteParamsRaw, type Router, type RouteRecordRaw } from "vue-router";

import { WebComponent } from "../../component/WebComponent";

export type ViewActivation = Promise<NavigationFailure | void | undefined>;

/**
 * A class to help with views.
 *
 * This class does not represent a view *per se*, it is only used to work with the corresponding view.
 * It is therefore safe to instantiate this class and use its functions, as this doesn't automatically create a new view.
 */
export abstract class View {
    protected readonly _router: Router;

    protected readonly _routeName: string;

    /**
     * @param name - The route name for this view.
     */
    protected constructor(name: string) {
        this._router = WebComponent.instance.router;

        this._routeName = name;
    }

    /**
     * Defines the route for this view.
     */
    public abstract route(): RouteRecordRaw;

    /**
     * Navigates to (= activates) this view.
     *
     * @param replace - Whether to replace the current browsing history entry.
     * @param query - Additional query (URL) parameters.
     * @param params - Additional URL placeholder parameters.
     *
     * @returns - A promise that can be used to react to page load events.
     */
    protected navigateTo(replace: boolean = false, query?: LocationQueryRaw, params?: RouteParamsRaw): ViewActivation {
        let to = { name: this._routeName, query: query, params: params };
        return replace ? this._router.replace(to) : this._router.push(to);
    }

    /**
     * The route name of this view.
     */
    public get name(): string {
        return this._routeName;
    }
}
