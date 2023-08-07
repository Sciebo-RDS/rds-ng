import "../../assets/styles/tailwind-init.css"

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
    private static _instance: Application | null = null;

    private readonly _vueApp: App<HostElement> | null = null;

    private constructor(appRoot: Component, appElement: string) {
        Application._instance = this;

        this._vueApp = this.createVueApp(appRoot, appElement);
    }

    private createVueApp(appRoot: Component, appElement: string) {
        let app = createApp(appRoot);

        app.use(createPinia());
        app.use(PrimeVue);

        app.mount(appElement);

        return app;
    }

    /**
     * The global Vue application instance.
     */
    public get vue() {
        return this._vueApp;
    }

    /**
     * Creates a new web application.
     *
     * If an instance already exists, an error is thrown.
     *
     * @param appRoot - The Vue root component.
     * @param appElement - The HTML element ID used for mounting the root component.
     *
     * @throws Error - If an application instance has already been created.
     */
    public static create(appRoot: Component, appElement: string = "#app") {
        if (Application._instance !== null) {
            throw new Error("An application instance has already been created");
        }

        return new Application(appRoot, appElement);
    }

    /**
     * The global ``Application`` instance.
     */
    public static get instance() {
        if (Application._instance === null) {
            throw new Error("No application instance has been created yet");
        }

        return Application._instance;
    }
}
