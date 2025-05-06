// This import needs to always be at the very top
import "reflect-metadata";

// Import the global styles.scss first
import "@assets/styles/styles.scss";

// Create the frontend component, which will automatically mount the main Vue App component
import { FrontendComponent } from "@/component/FrontendComponent";

const comp = new FrontendComponent();

// Mount the Vue application
comp.mount();
