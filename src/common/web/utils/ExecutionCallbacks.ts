/**
 * Helper class for running 'Done' and 'Failed' callbacks during arbitrary executions.
 */
export class ExecutionCallbacks<DoneCallback extends Function, FailCallback extends Function> {
    private _doneCallbacks: DoneCallback[] = [];
    private _failCallbacks: FailCallback[] = [];

    public constructor() {}

    /**
     * Adds a *Done* callback.
     *
     * @param cb - The callback to add.
     *
     * @returns - This instance to allow call chaining.
     */
    public done(cb: DoneCallback): this {
        this._doneCallbacks.push(cb);
        return this;
    }

    /**
     * Adds a *Fail* callback.
     *
     * @param cb - The callback to add.
     *
     * @returns - This instance to allow call chaining.
     */
    public failed(cb: FailCallback): this {
        this._failCallbacks.push(cb);
        return this;
    }

    /**
     * Invokes all *Done* callbacks.
     *
     * @param args - Arguments passed to the callbacks.
     */
    public invokeDoneCallbacks(...args: any[]): void {
        for (const callback of this._doneCallbacks) {
            callback(...args);
        }
    }

    /**
     * Invokes all *Fail* callbacks.
     *
     * @param args - Arguments passed to the callbacks.
     */
    public invokeFailCallbacks(...args: any[]): void {
        for (const callback of this._failCallbacks) {
            callback(...args);
        }
    }

    /**
     * Removecs all callbacks.
     */
    public reset(): void {
        this._doneCallbacks = [];
        this._failCallbacks = [];
    }

    /**
     * All *Done* callbacks.
     */
    public get doneCallbacks(): DoneCallback[] {
        return this._doneCallbacks;
    }

    /**
     * All *Fail* callbacks.
     */
    public get failCallbacks(): FailCallback[] {
        return this._failCallbacks;
    }
}
