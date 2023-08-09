// Always start by importing the desired PrimeVue theme
import "primevue/resources/themes/lara-light-indigo/theme.css";

import App from "./App.vue";
import { Component } from "@common/component/Component";
import { UnitID } from "@common/utils/UnitID";

import configData from "/config/config.toml?url&raw"

// Create a new web component and mount the main Vue App component
Component.create(new UnitID("client", "frontend"), App);

console.log(configData);
