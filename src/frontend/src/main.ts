// This import needs to always be at the very top
import "reflect-metadata";

// Import your desired PrimeVue theme next
import "primevue/resources/themes/lara-light-indigo/theme.css";

// And now for the actual component
import { Component } from "@common/component/Component";
import { UnitID } from "@common/utils/UnitID";

import App from "./App.vue";

// Create a new web component and mount the main Vue App component
const comp = Component.create(import.meta.env, new UnitID("client", "frontend"), App);
