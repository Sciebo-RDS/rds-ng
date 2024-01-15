import { defineStore } from "pinia";
import { ref } from "vue";

import { UserConfiguration } from "@common/data/entities/user/UserConfiguration";

/**
 * The user store for all user-specific data.
 *
 * @param configuration - The user configuration.
 */
export const userStore = defineStore("userStore", () => {
    const configuration = ref(new UserConfiguration());

    function reset(): void {
        configuration.value = new UserConfiguration();
    }

    return {
        configuration,
        reset
    };
});
