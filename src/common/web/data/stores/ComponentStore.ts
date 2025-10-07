import { defineStore } from "pinia";
import { ref } from "vue";
import { getURLQueryParam } from "../../utils/URLUtils";

/**
 * The overall state of the component:
 *     - **Initializing**: The component is initializing (initial state)
 *     - **Running**: The component is up and running, ready to be used
 *     - **ConnectionLost**: The connection to the server has been lost
 *     - **ConnectionError**: An error has occurred while connecting
 */
export const enum ComponentState {
    Connecting = "connecting",
    ConnectionLost = "connection-lost",
    ConnectionError = "connection-error",
    Running = "running"
}

/**
 * The global store for all component-related data.
 *
 * @param componentState - The overall state of the component.
 * @param componentStateMessage - An additional message about the component state.
 */
export const useComponentStore = defineStore("componentStore", () => {
    const componentState = ref(ComponentState.Connecting);
    const componentStateMessage = ref("");

    const queryParams = ref(new URLSearchParams());

    function getHostInstanceID(): string {
        return getURLQueryParam("instance-id") || "default";
    }

    function reset(): void {
        componentState.value = ComponentState.Connecting;
        componentStateMessage.value = "";

        queryParams.value = new URLSearchParams();
    }

    return {
        componentState,
        componentStateMessage,
        getHostInstanceID,
        queryParams,
        reset
    };
});
