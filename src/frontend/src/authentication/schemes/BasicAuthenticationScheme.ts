import { useUserStore } from "@/data/stores/UserStore";
import { defineAsyncComponent } from "vue";

import { createUserToken, isUserTokenValid } from "@common/data/entities/user/UserToken";

import { AuthenticationScheme } from "@/authentication/AuthenticationScheme";
import { Authenticator } from "@/authentication/Authenticator";
import { FrontendComponent } from "@/component/FrontendComponent";

/**
 * Basic authentication using a simple username.
 */
export class BasicAuthenticationScheme extends AuthenticationScheme {
    public static readonly Scheme = "basic";

    public constructor(comp: FrontendComponent) {
        super(
            comp,
            BasicAuthenticationScheme.Scheme,
            defineAsyncComponent(() => import("@/ui/authentication/BasicAuthentication.vue")),
        );
    }

    public authenticator(userName: string): Authenticator {
        return new Authenticator(this._component, createUserToken(userName, userName));
    }

    public enter(): void {
        super.enter();

        this.reauthenticate();
    }

    private reauthenticate(): void {
        // Resend the user authentication information
        const { userToken } = useUserStore();

        if (isUserTokenValid(userToken)) {
            this.authenticator(userToken.user_id).authenticate();
        }
    }
}
