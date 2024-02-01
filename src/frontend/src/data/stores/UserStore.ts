import { defineStore } from "pinia";
import { ref } from "vue";

import { UserSettings } from "@common/data/entities/user/UserSettings";

/**
 * The user store for all user-specific data.
 *
 * @param settings - The user settings.
 */
export const useUserStore = defineStore("userStore", () => {
    const userIDToken = ref<string | undefined>(undefined);

    const userSettings = ref(new UserSettings());

    function reset(): void {
        userIDToken.value = undefined;

        userSettings.value = new UserSettings();
    }

    return {
        userIDToken,
        userSettings,
        reset
    };
});
