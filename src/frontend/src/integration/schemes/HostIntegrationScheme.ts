import { defineAsyncComponent } from "vue";

import { createUserToken } from "@common/data/entities/user/UserToken";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { Authenticator } from "@/integration/Authenticator";
import { Authorizer } from "@/integration/Authorizer";
import { IntegrationScheme } from "@/integration/IntegrationScheme";
import { type HostUserToken } from "@/integration/HostTypes";

/**
 * Basic authentication using a simple username.
 */
export class HostIntegrationScheme extends IntegrationScheme {
    public static readonly Scheme = "host";

    public constructor(comp: FrontendComponent) {
        super(
            comp,
            HostIntegrationScheme.Scheme,
            defineAsyncComponent(() => import("@/ui/integration/HostIntegration.vue")),
        );
    }

    public authenticator(token: HostUserToken): Authenticator {
        return new Authenticator(this._component, createUserToken(token.userID, token.userName));
    }

    public authorizer(): Authorizer {
        return new Authorizer(this._component);
    }

    public enter(): void {
        super.enter();

        this.resetUserToken();
    }

    public leave(): void {
        super.leave();

        this.resetUserToken();
    }

    private resetUserToken(): void {
        // Enforce a re-authentication on each refresh to avoid user hijacking
        const { resetUserToken } = useUserStore();
        resetUserToken();
    }
}
