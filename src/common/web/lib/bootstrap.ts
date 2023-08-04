import { Component } from "vue";
import { Application } from "./app/Application";
import { useApplicationStore } from "./app/ApplicationStore";

import "../assets/styles/tailwind-init.css"

/**
 * Performs all initialization tasks for a web application and returns the newly created ``Application`` instance.
 *
 * @param appRoot - The Vue root component.
 * @param appElement - The HTML element ID used for mounting the root component.
 *
 * @returns - The newly created ``Application`` object.
 */
export default function bootstrap(appRoot: Component, appElement: string = "#app"): Application {
    let app = new Application(appRoot, appElement);

    let appStore = useApplicationStore();
    appStore.app = app;

    return app;
}
