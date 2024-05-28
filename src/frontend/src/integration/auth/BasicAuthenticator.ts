import { createUserToken } from "@common/data/entities/user/UserToken";

import { FrontendComponent } from "@/component/FrontendComponent";
import { Authenticator } from "@/integration/auth/Authenticator";

/**
 * Authenticator for basic integration.
 */
export class BasicAuthenticator extends Authenticator {
    public constructor(comp: FrontendComponent, userName: string) {
        super(comp, createUserToken(userName, userName));
    }

    public authenticate(): void {
        this.authenticateWithToken();
    }
}
