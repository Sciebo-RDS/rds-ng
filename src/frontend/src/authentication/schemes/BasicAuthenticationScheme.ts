import { defineAsyncComponent } from "vue";

import { AuthenticationScheme } from "@/authentication/AuthenticationScheme";
import { Authenticator } from "@/authentication/Authenticator";
import { createUserToken } from "@/authentication/UserToken";
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
            defineAsyncComponent(() => import("@/ui/authentication/BasicAuthentication.vue"))
        );
    }

    public authenticator(userName: string): Authenticator {
        return new Authenticator(this._component, createUserToken(userName, userName));
    }
}
