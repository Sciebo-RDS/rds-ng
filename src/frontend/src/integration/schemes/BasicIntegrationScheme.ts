import { defineAsyncComponent } from "vue";

import { createUserToken, isUserTokenValid } from "@common/data/entities/user/UserToken";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { Authenticator } from "@/integration/Authenticator";
import { Authorizer } from "@/integration/Authorizer";
import { IntegrationScheme } from "@/integration/IntegrationScheme";

/**
 * Basic authentication using a simple username.
 */
export class BasicIntegrationScheme extends IntegrationScheme {
    public static readonly Scheme = "basic";

    public constructor(comp: FrontendComponent) {
        super(
            comp,
            BasicIntegrationScheme.Scheme,
            defineAsyncComponent(() => import("@/ui/integration/BasicIntegration.vue")),
        );
    }

    public authenticator(userName: string): Authenticator {
        return new Authenticator(this._component, createUserToken(userName, userName));
    }

    public authorizer(): Authorizer {
        return new Authorizer(this._component);
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
