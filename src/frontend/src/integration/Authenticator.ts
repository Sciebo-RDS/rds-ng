import { storeToRefs } from "pinia";

import { AuthenticateUserCommand } from "@common/api/user/UserCommands";
import { isUserTokenValid, type UserToken } from "@common/data/entities/user/UserToken";
import { useNetworkStore } from "@common/data/stores/NetworkStore";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { IntegrationPerformer } from "@/integration/IntegrationPerformer";

export class Authenticator extends IntegrationPerformer {
    private readonly _userToken: UserToken;

    public constructor(comp: FrontendComponent, token: UserToken) {
        super(comp);

        this._userToken = token;
    }

    /**
     * Authenticate the user.
     */
    public authenticate(): void {
        if (!isUserTokenValid(this._userToken)) {
            throw new Error("Invalid user token used for authentication");
        }

        const nwStore = useNetworkStore();

        AuthenticateUserCommand.build(this._component.frontendService.messageBuilder, this._userToken)
            .done((_, success, msg) => {
                if (success) {
                    const userStore = useUserStore();
                    const { userToken } = storeToRefs(userStore);

                    userToken.value = this._userToken;

                    this.callDoneCallbacks();
                } else {
                    this.callFailCallbacks(msg);
                }
            })
            .failed((_, msg: string) => {
                this.callFailCallbacks(msg);
            })
            .emit(nwStore.serverChannel);
    }
}
