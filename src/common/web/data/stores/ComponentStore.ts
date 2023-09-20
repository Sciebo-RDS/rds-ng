import { defineStore } from "pinia";
import { ref } from "vue";

/**
 * The overall state of the component:
 *     - **Initializing**: The component is initializing (initial state)
 *     - **Running**: The component is up and running, ready to be used
 *     - **ConnectionLost**: The connection to the server has been lost
 */
export const enum ComponentState {
    Initializing = "initializing",
    Running = "running",
    ConnectionLost = "connection-lost",
    ConnectionError = "connection-error",
}

/**
 * The global store for all component-related data.
 *
 * @param componentState - The overall state of the component.
 * @param componentStateMessage - An additional message about the component state.
 */
export const componentStore = defineStore("componentStore", () => {
    const componentState = ref(ComponentState.Initializing);
    const componentStateMessage = ref("");

    function reset() {
        componentState.value = ComponentState.Initializing;
        componentStateMessage.value = "";
    }

    return {
        componentState,
        componentStateMessage,
        reset
    };
});
