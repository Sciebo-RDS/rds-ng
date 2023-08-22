import { defineStore } from "pinia";
import { ref } from "vue";

/**
 * The global store for all network-related data.
 *
 * @param connected - Whether the client is connected to a server.
 */
export const networkStore = defineStore("networkStore", () => {
    const connected = ref(false);

    return { connected };
});
