import { createUserToken } from "@common/data/entities/user/UserToken";

import { FrontendComponent } from "@/component/FrontendComponent";
import { Authenticator } from "@/integration/authentication/Authenticator";
import { type HostUserToken } from "@/integration/HostTypes";

/**
 * Authenticator for host integration.
 */
export class HostAuthenticator extends Authenticator {
    public constructor(comp: FrontendComponent, userToken: HostUserToken) {
        super(comp, createUserToken(userToken.userID, userToken.userName));
    }

    public authenticate(): void {
        this.authenticateWithToken();
    }
}
