import { defineStore } from "pinia";
import { ref } from "vue";

import { UserSettings } from "@common/data/entities/user/UserSettings";

import { FrontendComponent } from "@/component/FrontendComponent";

/**
 * The user store for all user-specific data.
 *
 * @param settings - The user settings.
 */
export const useUserStore = defineStore("userStore", () => {
    const comp = FrontendComponent.inject();

    const userToken = comp.session.sessionValue<string | undefined>("user-token", undefined);
    const userSettings = ref(new UserSettings());

    function reset(): void {
        userToken.value = undefined;

        userSettings.value = new UserSettings();
    }

    return {
        userToken,
        userSettings,
        reset
    };
});
