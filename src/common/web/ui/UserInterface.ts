import { type Component as VueComponent } from "vue";
import { type Router } from "vue-router";

import { MainView } from "./views/main/MainView";

/**
 * Class for overall user interface handling.
 */
export class UserInterface {
    private readonly _mainView: MainView;

    /**
     * @param router - The Vue router.
     * @param appRoot - The root (main) application component.
     */
    public constructor(router: Router, appRoot: VueComponent) {
        this._mainView = new MainView(router, appRoot);
    }

    /**
     * The main view.
     */
    public get mainView(): MainView {
        return this._mainView;
    }
}
