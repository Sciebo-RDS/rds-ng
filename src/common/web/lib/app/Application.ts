import { Component, createApp } from "vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

/**
 * Base class for all web applications.
 *
 * Web applications are always based on this class. It mainly maintains an instance of the ``Core``, but also stores general information
 * about the application itself and the entire project.
 *
 * Instances of this class are never created directly. Instead, always use the ``bootstrap`` function which performs all necessary initialization
 * tasks.
 */
export class Application {
    private readonly _vueApp: App<HostElement> | null = null;

    /**
     * Creates a new web application.
     *
     * @param appRoot - The Vue root component.
     * @param appElement - The HTML element ID used for mounting the root component.
     */
    public constructor(appRoot: Component, appElement: string) {
        this._vueApp = this.createVueApp(appRoot, appElement);
    }

    private createVueApp(appRoot: Component, appElement: string): App<HostElement> {
        let app = createApp(appRoot);

        app.use(createPinia());
        app.use(PrimeVue);

        app.mount(appElement);

        return app;
    }

    /**
     * The global Vue application instance.
     */
    public get vue(): App<HostElement> {
        return this._vueApp;
    }
}
