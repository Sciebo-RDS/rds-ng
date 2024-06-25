import { defineStore } from "pinia";
import { ref } from "vue";

/**
 * Frontend store for general application data.
 */
export const useFrontendStore = defineStore("frontendStore", () => {
    const initializationMessage = ref("");
    const initializationError = ref(false);

    function reset(): void {
        initializationMessage.value = "";
        initializationError.value = false;
    }

    return {
        initializationMessage,
        initializationError,
        reset,
    };
});
