import { defineStore } from "pinia";
import { ref } from "vue";

import { UserSettings } from "@common/data/entities/user/UserSettings";

/**
 * The user store for all user-specific data.
 *
 * @param settings - The user settings.
 */
export const userStore = defineStore("userStore", () => {
    const settings = ref(new UserSettings());

    function reset(): void {
        settings.value = new UserSettings();
    }

    return {
        settings,
        reset
    };
});
