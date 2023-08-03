import { App, Component, createApp } from "vue"
import { createPinia } from "pinia"

import PrimeVue from "primevue/config"

import "../../assets/styles/tailwind-init.css"
import "primevue/resources/themes/lara-light-indigo/theme.css"

function createApplication(appRoot: Component, appElement: string = "#app"): App {
    const app = createApp(appRoot);

    app.use(createPinia());
    app.use(PrimeVue);

    app.mount(appElement);

    return app;
}

export default createApplication;
