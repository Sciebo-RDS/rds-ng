import { defineAsyncComponent } from "vue";

import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";
import { isUserTokenValid } from "@common/data/entities/user/UserToken";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { Authenticator } from "@/integration/authentication/Authenticator";
import { BasicAuthenticator } from "@/integration/authentication/BasicAuthenticator";
import { Authorizer } from "@/integration/authorization/Authorizer";
import { BasicAuthorizer } from "@/integration/authorization/BasicAuthorizer";
import { BasicResourcesBroker } from "@/integration/resources/brokers/BasicResourcesBroker";
import { ResourcesBroker } from "@/integration/resources/brokers/ResourcesBroker";
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
        return new BasicAuthenticator(this._component, userName);
    }

    public authorizer(): Authorizer {
        return new BasicAuthorizer(this._component);
    }

    public resourcesBroker(): ResourcesBroker {
        return new BasicResourcesBroker(this._component);
    }

    public enter(): void {
        super.enter();

        this.reAuth();
    }

    private reAuth(): void {
        // Resend the user authentication information
        const { userToken } = useUserStore();
        if (isUserTokenValid(userToken)) {
            this.authenticator(userToken.user_id).authenticate();
        }

        // Redo the authorization and broker assignment
        this.authorizer().authorize(AuthorizationState.Authorized, "");
        this.resourcesBroker().assign();
    }
}
