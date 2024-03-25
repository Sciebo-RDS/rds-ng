import { defineStore } from "pinia";
import { ref } from "vue";

import { type UserToken } from "@common/authentication/UserToken";
import { UserSettings } from "@common/data/entities/user/UserSettings";

import { FrontendComponent } from "@/component/FrontendComponent";

/**
 * The user store for all user-specific data.
 *
 * @param settings - The user settings.
 */
export const useUserStore = defineStore("userStore", () => {
    const comp = FrontendComponent.inject();

    const userToken = comp.session.sessionValue<UserToken>("user-token", {} as UserToken);
    const userSettings = ref(new UserSettings());

    function reset(): void {
        userToken.value = {} as UserToken;
        userSettings.value = new UserSettings();
    }

    function resetUserToken(): void {
        userToken.value = {} as UserToken;
    }

    return {
        userToken,
        userSettings,
        reset,
        resetUserToken,
    };
});
