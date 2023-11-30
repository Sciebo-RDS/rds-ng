import { type LocationQueryRaw, type RouteParamsRaw, type Router, type RouteRecordRaw } from "vue-router";

/**
 * A class to help with routed views.
 *
 * This class does not represent a view *per se*, it is only used to work with the corresponding view.
 * It is therefore safe to instantiate this class and use its functions, as this doesn't automatically create a new view.
 */
export abstract class View {
    protected readonly _router: Router;
    protected readonly _routeName: string;
    protected readonly _routeOptions: RouteRecordRaw | undefined;

    protected readonly _subViews: View[] | undefined;

    /**
     * @param router - The Vue router.
     * @param name - The route name for this view.
     * @param routeOptions - Additional route options.
     * @param subViews - Optional sub-views of this view.
     */
    protected constructor(router: Router, name: string, routeOptions?: RouteRecordRaw, subViews?: View[]) {
        this._router = router;
        this._routeName = name;
        this._routeOptions = routeOptions;

        this._subViews = subViews;

        this.mountRoute(router);
    }

    protected mountRoute(router: Router): void {
        router.addRoute(this.route());
    }

    /**
     * Gets the route of this view.
     */
    public route(): RouteRecordRaw {
        let route = this.defineRoute();
        if (this._subViews?.length) {
            route.children = this._subViews.map((view) => view.route());
        }
        if (this._routeOptions) {
            route = { ...route, ...this._routeOptions } as RouteRecordRaw;
        }
        return route;
    }

    /**
     * Defines the route for this view.
     */
    protected abstract defineRoute(): RouteRecordRaw;

    /**
     * Navigates to (= activates) this view.
     *
     * @param replace - Whether to replace the current browsing history entry.
     * @param query - Additional query (URL) parameters.
     * @param params - Additional URL placeholder parameters.
     *
     * @returns - A promise that can be used to react to page load events.
     */
    public navigateTo(replace: boolean = false, query?: LocationQueryRaw, params?: RouteParamsRaw): void {
        let to = { name: this._routeName, query: query, params: params };
        replace ? this._router.replace(to).then() : this._router.push(to).then();
    }

    /**
     * The route name of this view.
     */
    public get name(): string {
        return this._routeName;
    }

    /**
     * The sub-views of the views.
     */
    public get subViews(): View[] {
        return this._subViews ? this._subViews : [];
    }
}
