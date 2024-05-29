import { defineAsyncComponent } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { Authenticator } from "@/integration/authentication/Authenticator";
import { Authorizer } from "@/integration/authorization/Authorizer";
import { HostAuthenticator } from "@/integration/authentication/HostAuthenticator";
import { HostAuthorizer } from "@/integration/authorization/HostAuthorizer";
import { IntegrationScheme } from "@/integration/IntegrationScheme";
import { type HostAuthorization, type HostUserToken } from "@/integration/HostTypes";

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
        return new HostAuthenticator(this._component, token);
    }

    public authorizer(hostAuth: HostAuthorization): Authorizer {
        return new HostAuthorizer(this._component, hostAuth);
    }

    public enter(): void {
        super.enter();

        this.resetAuth();
    }

    public leave(): void {
        super.leave();

        this.resetAuth();
    }

    private resetAuth(): void {
        // Enforce a re-authentication on each refresh to avoid user hijacking
        const { resetAuth } = useUserStore();
        resetAuth();
    }
}
