// This import needs to always be at the very top
import "reflect-metadata";

// Import the global styles.scss first, then your desired theme
import "@assets/styles/styles.scss";
import "@assets/styles/themes/light-theme.scss";

// Create the frontend component, which will automatically mount the main Vue App component
import { FrontendComponent } from "@/component/FrontendComponent";

const comp = new FrontendComponent();

// Mount the Vue application
comp.mount();
