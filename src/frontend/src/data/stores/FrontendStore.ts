import { defineStore } from "pinia";
import { ref } from "vue";

export const enum DisplayState {
    Landing,
    Project
}

/**
 * Frontend store for general application data.
 */
export const useFrontendStore = defineStore("frontendStore", () => {
    const initializationMessage = ref("");
    const initializationError = ref(false);

    const displayState = ref(DisplayState.Landing);

    function reset(): void {
        initializationMessage.value = "";
        initializationError.value = false;

        displayState.value = DisplayState.Landing;
    }

    return {
        initializationMessage,
        initializationError,
        displayState,
        reset
    };
});
