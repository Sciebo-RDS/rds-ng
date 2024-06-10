import { defineStore } from "pinia";
import { ref } from "vue";

import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";
import { UserSettings } from "@common/data/entities/user/UserSettings";
import { type UserToken } from "@common/data/entities/user/UserToken";

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

    const authorizationState = ref(AuthorizationState.NotAuthorized);

    function reset(): void {
        userToken.value = {} as UserToken;
        userSettings.value = new UserSettings();

        authorizationState.value = AuthorizationState.NotAuthorized;
    }

    function resetAuth(): void {
        userToken.value = {} as UserToken;

        authorizationState.value = AuthorizationState.NotAuthorized;
    }

    return {
        userToken,
        userSettings,
        authorizationState,
        reset,
        resetAuth,
    };
});
