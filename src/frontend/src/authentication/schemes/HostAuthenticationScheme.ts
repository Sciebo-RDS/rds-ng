import { createUserToken } from "@/authentication/UserToken";
import { defineAsyncComponent } from "vue";

import { Authenticator } from "@/authentication/Authenticator";
import { AuthenticationScheme } from "@/authentication/AuthenticationScheme";
import { FrontendComponent } from "@/component/FrontendComponent";
import { type HostUserToken } from "@/integration/HostUserToken";

/**
 * Basic authentication using a simple username.
 */
export class HostAuthenticationScheme extends AuthenticationScheme {
    public static readonly Scheme = "host";

    public constructor(comp: FrontendComponent) {
        super(
            comp,
            HostAuthenticationScheme.Scheme,
            defineAsyncComponent(() => import("@/ui/misc/authentication/HostAuthentication.vue"))
        );
    }

    public authenticator(token: HostUserToken): Authenticator {
        return new Authenticator(this._comp, createUserToken(token.userID, token.userName));
    }
}
