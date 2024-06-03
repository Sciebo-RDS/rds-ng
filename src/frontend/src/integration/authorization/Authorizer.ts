import { storeToRefs } from "pinia";

import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";
import { ExecutionCallbacks } from "@common/utils/ExecutionCallbacks";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";

export type AuthorizerDoneCallback = () => void;
export type AuthorizerFailCallback = (msg: string) => void;

/**
 * Base authorizer.
 */
export abstract class Authorizer {
    protected readonly _component: FrontendComponent;

    protected readonly _callbacks = new ExecutionCallbacks<AuthorizerDoneCallback, AuthorizerFailCallback>();

    protected constructor(comp: FrontendComponent) {
        this._component = comp;
    }

    /**
     * Authorize the user/integration.
     *
     * @param authState - The current authorization state.
     */
    public abstract authorize(authState: AuthorizationState): void;

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

    protected setAuthorized(authorized: boolean, msg: string = ""): void {
        const userStore = useUserStore();
        const { authorizationState } = storeToRefs(userStore);

        authorizationState.value = authorized ? AuthorizationState.Authorized : AuthorizationState.NotAuthorized;

        if (authorized) {
            this._callbacks.invokeDoneCallbacks();
        } else {
            this._callbacks.invokeFailCallbacks(msg);
        }
    }
}
