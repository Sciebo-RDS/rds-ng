import { FrontendComponent } from "@/component/FrontendComponent";
import { useFrontendStore } from "@/data/stores/FrontendStore";

/**
 * Tools for working with the frontend.
 */
export function useFrontendTools(comp: FrontendComponent) {
    function setInitializationMessage(message: string, isError: boolean = false) {
        const frontendStore = useFrontendStore();

        frontendStore.initializationMessage = message;
        frontendStore.initializationError = isError;
    }

    return {
        setInitializationMessage,
    };
}
