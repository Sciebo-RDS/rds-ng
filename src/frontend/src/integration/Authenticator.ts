import { storeToRefs } from "pinia";

import { AuthenticateUserCommand } from "@common/api/user/UserCommands";
import { isUserTokenValid, type UserToken } from "@common/data/entities/user/UserToken";
import { useNetworkStore } from "@common/data/stores/NetworkStore";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";

export type AuthDoneCallback = () => void;
export type AuthFailCallback = (msg: string) => void;

export class Authenticator {
    private readonly _component: FrontendComponent;

    private readonly _userToken: UserToken;

    private _doneCallbacks: AuthDoneCallback[] = [];
    private _failCallbacks: AuthFailCallback[] = [];

    public constructor(comp: FrontendComponent, token: UserToken) {
        this._component = comp;

        this._userToken = token;
    }

    /**
     * Adds a *Done* callback.
     *
     * @param cb - The callback to add.
     *
     * @returns - This authenticator instance to allow call chaining.
     */
    public done(cb: AuthDoneCallback): this {
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
    public failed(cb: AuthFailCallback): this {
        this._failCallbacks.push(cb);
        return this;
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

    private callDoneCallbacks(): void {
        for (const callback of this._doneCallbacks) {
            callback();
        }
    }

    private callFailCallbacks(msg: string): void {
        for (const callback of this._failCallbacks) {
            callback(msg);
        }
    }
}
