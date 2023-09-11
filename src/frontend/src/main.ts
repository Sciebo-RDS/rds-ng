// This import needs to always be at the very top
import "reflect-metadata";

// Import your desired PrimeVue theme next
import "primevue/resources/themes/lara-light-blue/theme.css";

// Create the frontend component, which will automatically mount the main Vue App component
import { FrontendComponent } from "@/component/FrontendComponent";

const comp = new FrontendComponent();
