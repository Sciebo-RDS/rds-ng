import { defineAsyncComponent } from "vue";

import { type AuthorizationSettings } from "@common/data/entities/authorization/AuthorizationSettings";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { Authenticator } from "@/integration/authentication/Authenticator";
import { HostAuthenticator } from "@/integration/authentication/HostAuthenticator";
import { Authorizer } from "@/integration/authorization/Authorizer";
import { HostAuthorizer } from "@/integration/authorization/HostAuthorizer";
import { HostResourcesBroker } from "@/integration/resources/brokers/HostResourcesBroker";
import { ResourcesBroker } from "@/integration/resources/brokers/ResourcesBroker";
import { type HostResources, type HostUserToken } from "@/integration/HostTypes";
import { IntegrationScheme } from "@/integration/IntegrationScheme";

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

    public authorizer(hostAuth: AuthorizationSettings): Authorizer {
        return new HostAuthorizer(this._component, hostAuth);
    }

    public resourcesBroker(hostResources: HostResources): ResourcesBroker {
        return new HostResourcesBroker(this._component, hostResources);
    }

    public enter(): void {
        super.enter();

        this.resetLogin();
    }

    public leave(): void {
        super.leave();

        this.resetLogin();
    }

    private resetLogin(): void {
        // Enforce a re-authentication on each refresh to avoid user hijacking
        const { resetLogin } = useUserStore();
        resetLogin();
    }
}
