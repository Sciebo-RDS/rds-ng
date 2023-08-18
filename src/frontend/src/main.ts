import { Component } from "@common/component/Component";
import { UnitID } from "@common/utils/UnitID";
import "primevue/resources/themes/lara-light-indigo/theme.css";

import App from "./App.vue";

// Create a new web component and mount the main Vue App component
const comp = Component.create(import.meta.env, new UnitID("client", "frontend"), App);
const svc = comp.createService("Frontend service");

comp.run();
