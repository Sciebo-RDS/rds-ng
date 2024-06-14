import { storeToRefs } from "pinia";

import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";
import { ExecutionCallbacks } from "@common/utils/ExecutionCallbacks";

import { useUserStore } from "@/data/stores/UserStore";
import { IntegrationHandler } from "@/integration/IntegrationHandler";

export type AuthorizerDoneCallback = () => void;
export type AuthorizerFailCallback = (msg: string) => void;

/**
 * Base authorizer.
 */
export abstract class Authorizer extends IntegrationHandler {
    protected readonly _callbacks = new ExecutionCallbacks<AuthorizerDoneCallback, AuthorizerFailCallback>();

    /**
     * Authorize the user/integration.
     *
     * @param authState - The current authorization state.
     * @param fingerprint - The user's fingerprint.
     */
    public abstract authorize(authState: AuthorizationState, fingerprint: string): void;

    /**
     * Adds a *Done* callback.
     *
     * @param cb - The callback to add.
     */
    public done(cb: AuthorizerDoneCallback): Authorizer {
        this._callbacks.done(cb);
        return this;
    }

    /**
     * Adds a *Fail* callback.
     *
     * @param cb - The callback to add.
     */
    public failed(cb: AuthorizerFailCallback): Authorizer {
        this._callbacks.failed(cb);
        return this;
    }

    protected setAuthorizationState(authState: AuthorizationState, msg: string = ""): void {
        const userStore = useUserStore();
        const { authorizationState } = storeToRefs(userStore);

        authorizationState.value = authState;

        if (authState == AuthorizationState.Authorized) {
            this._callbacks.invokeDoneCallbacks();
        } else {
            this._callbacks.invokeFailCallbacks(msg);
        }
    }
}
