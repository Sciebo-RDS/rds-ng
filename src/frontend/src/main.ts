// Always start by importing the desired PrimeVue theme
import "primevue/resources/themes/lara-light-indigo/theme.css";

import App from "./App.vue";
import { Component } from "@common/component/Component";
import { UnitID } from "@common/utils/UnitID";

// Create a new web component and mount the main Vue App component
Component.create(import.meta.env, new UnitID("client", "frontend"), App);
