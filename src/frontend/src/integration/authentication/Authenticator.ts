import { storeToRefs } from "pinia";

import { AuthenticateUserCommand, AuthenticateUserReply } from "@common/api/user/UserCommands";
import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";
import { isUserTokenValid, type UserToken } from "@common/data/entities/user/UserToken";
import { useNetworkStore } from "@common/data/stores/NetworkStore";
import { ExecutionCallbacks } from "@common/utils/ExecutionCallbacks";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";

export type AuthenticatorDoneCallback = (authState: AuthorizationState) => void;
export type AuthenticatorFailCallback = (msg: string) => void;

/**
 * Base authenticator.
 */
export abstract class Authenticator {
    protected readonly _component: FrontendComponent;

    protected readonly _userToken: UserToken;

    protected readonly _callbacks = new ExecutionCallbacks<AuthenticatorDoneCallback, AuthenticatorFailCallback>();

    protected constructor(comp: FrontendComponent, token: UserToken) {
        this._component = comp;

        this._userToken = token;
    }

    /**
     * Authenticate the user.
     */
    public abstract authenticate(): void;

    /**
     * Adds a *Done* callback.
     *
     * @param cb - The callback to add.
     */
    public done(cb: AuthenticatorDoneCallback): Authenticator {
        this._callbacks.done(cb);
        return this;
    }

    /**
     * Adds a *Fail* callback.
     *
     * @param cb - The callback to add.
     */
    public failed(cb: AuthenticatorFailCallback): Authenticator {
        this._callbacks.failed(cb);
        return this;
    }

    protected authenticateWithToken(): void {
        if (!isUserTokenValid(this._userToken)) {
            throw new Error("Invalid user token used for authentication");
        }

        const nwStore = useNetworkStore();

        AuthenticateUserCommand.build(this._component.frontendService.messageBuilder, this._userToken)
            .done((reply: AuthenticateUserReply, success, msg) => {
                if (success) {
                    const userStore = useUserStore();
                    const { userToken } = storeToRefs(userStore);

                    userToken.value = this._userToken;

                    this._callbacks.invokeDoneCallbacks(reply.is_authorized ? AuthorizationState.Authorized : AuthorizationState.NotAuthorized);
                } else {
                    this._callbacks.invokeFailCallbacks(msg);
                }
            })
            .failed((_, msg: string) => {
                this._callbacks.invokeFailCallbacks(msg);
            })
            .emit(nwStore.serverChannel);
    }
}