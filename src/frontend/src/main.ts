// Always start by importing the desired PrimeVue theme
import "primevue/resources/themes/lara-light-indigo/theme.css"

import App from "./App.vue"
import { Component } from "@common/lib/component/Component";
import { UnitID } from "@common/lib/utils/UnitID";

// Create a new web component and mount the main Vue App component
Component.create(new UnitID("client", "web-frontend"), App);
