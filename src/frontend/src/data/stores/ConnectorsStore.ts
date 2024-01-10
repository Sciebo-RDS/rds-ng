import { defineStore } from "pinia";
import { ref } from "vue";

import { Connector } from "@common/data/entities/Connector";

/**
 * The connectors store for all connector-specific data.
 *
 * @param connectors - List of all connectors.
 */
export const connectorsStore = defineStore("connectorsStore", () => {
    const connectors = ref<Connector[]>([]);

    function reset(): void {
        connectors.value = [] as Connector[];
    }

    return {
        connectors,
        reset
    };
});
