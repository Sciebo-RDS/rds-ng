import { type Component as VueComponent } from "vue";
import { type Router, type RouteRecordRaw } from "vue-router";

import { MainView } from "./views/main/MainView";
import { View } from "./views/View";

/**
 * Class for overall user interface handling.
 */
export class UserInterface {
    protected readonly _mainView: MainView;

    /**
     * @param router - The Vue router.
     * @param appRoot - The root (main) application component.
     */
    public constructor(router: Router, appRoot: VueComponent) {
        this._mainView = new MainView(router, appRoot, this.configureMainRoute(), this.createSubViews(router));
    }

    /**
     * Supply additional options for the main route.
     *
     * @returns - Additional route options.
     */
    protected configureMainRoute(): RouteRecordRaw | undefined {
        return undefined;
    }

    /**
     * Creates additional sub-views of the main view.
     *
     * @returns - An array of all direct sub-views.
     */
    protected createSubViews(router: Router): View[] {
        return [];
    }

    /**
     * The main view.
     */
    public get mainView(): MainView {
        return this._mainView;
    }
}
