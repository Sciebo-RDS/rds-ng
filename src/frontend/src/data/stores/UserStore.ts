import { useSessionStorage } from "@vueuse/core";
import { defineStore } from "pinia";
import { ref } from "vue";

import { UserSettings } from "@common/data/entities/user/UserSettings";

import { FrontendComponent } from "@/component/FrontendComponent";
import { FrontendSettingIDs } from "@/settings/FrontendSettingIDs";

/**
 * The user store for all user-specific data.
 *
 * @param settings - The user settings.
 */
export const useUserStore = defineStore("userStore", () => {
    const comp = FrontendComponent.inject();

    const userToken = useSessionStorage(comp.data.config.value<string>(FrontendSettingIDs.UserTokenKey), undefined);
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
