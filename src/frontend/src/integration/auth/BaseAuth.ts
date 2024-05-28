import { FrontendComponent } from "@/component/FrontendComponent";

export type PerformerDoneCallback = () => void;
export type PerformerFailCallback = (msg: string) => void;

/**
 * Base class for both authenticators and authorizers.
 */
export abstract class BaseAuth {
    protected readonly _component: FrontendComponent;

    private _doneCallbacks: PerformerDoneCallback[] = [];
    private _failCallbacks: PerformerFailCallback[] = [];

    protected constructor(comp: FrontendComponent) {
        this._component = comp;
    }

    /**
     * Adds a *Done* callback.
     *
     * @param cb - The callback to add.
     *
     * @returns - This authenticator instance to allow call chaining.
     */
    public done(cb: PerformerDoneCallback): this {
        this._doneCallbacks.push(cb);
        return this;
    }

    /**
     * Adds a *Fail* callback.
     *
     * @param cb - The callback to add.
     *
     * @returns - This authenticator instance to allow call chaining.
     */
    public failed(cb: PerformerFailCallback): this {
        this._failCallbacks.push(cb);
        return this;
    }

    protected callDoneCallbacks(): void {
        for (const callback of this._doneCallbacks) {
            callback();
        }
    }

    protected callFailCallbacks(msg: string): void {
        for (const callback of this._failCallbacks) {
            callback(msg);
        }
    }
}
