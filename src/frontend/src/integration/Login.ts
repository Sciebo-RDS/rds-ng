import { storeToRefs } from "pinia";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { type UserToken } from "@/integration/UserToken";
import { SetSessionValueAction } from "@/ui/actions/session/SetSessionValueAction";

/**
 * The supported login types.
 *
 * @param Basic - Use a basic login form.
 * @param Host - The host system provides a login token.
 */
export const enum LoginType {
    Basic = "basic",
    Host = "host"
}

export type LoginSuccessCallback = () => void;
export type LoginFailureCallback = (msg: string) => void;

export function useLogin(comp: FrontendComponent) {
    function login(token: UserToken, succeeded?: LoginSuccessCallback, failed?: LoginFailureCallback): void {
        const action = new SetSessionValueAction(comp, true);
        action.prepare("user-token", token.userID).done((_, success, msg) => {
            if (success) {
                const userStore = useUserStore();
                const { userToken } = storeToRefs(userStore);

                userToken.value = token;

                if (succeeded) {
                    succeeded();
                }
            } else {
                if (failed) {
                    failed(msg);
                }
            }
        }).failed((_, msg: string) => {
            if (failed) {
                failed(msg);
            }
        });
        action.execute();
    }

    return {
        login
    };
}
