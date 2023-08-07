// Always start by importing the desired PrimeVue theme
import "primevue/resources/themes/lara-light-indigo/theme.css"

import App from "./App.vue"
import { Application } from "@common/lib/app/Application";

// Create a new application and mount the main Vue App component
Application.create(App);
