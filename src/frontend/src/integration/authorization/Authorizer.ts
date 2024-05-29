import { storeToRefs } from "pinia";

import { ExecutionCallbacks } from "@common/utils/ExecutionCallbacks";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";

export type AuthorizerDoneCallback = () => void;
export type AuthorizerFailCallback = (msg: string) => void;

/**
 * Base authorizer.
 */
export abstract class Authorizer {
    private readonly _component: FrontendComponent;

    private readonly _callbacks: ExecutionCallbacks<AuthorizerDoneCallback, AuthorizerFailCallback> = new ExecutionCallbacks();

    protected constructor(comp: FrontendComponent) {
        this._component = comp;
    }

    /**
     * Authorize the user/integration.
     */
    public abstract authorize(): void;

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
        const { isAuthorized } = storeToRefs(userStore);

        isAuthorized.value = authorized;

        if (authorized) {
            this._callbacks.invokeDoneCallbacks();
        } else {
            this._callbacks.invokeFailCallbacks(msg);
        }
    }
}
