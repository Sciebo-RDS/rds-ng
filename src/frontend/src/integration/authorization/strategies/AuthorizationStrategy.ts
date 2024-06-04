import { RequestAuthorizationCommand } from "@common/api/authorization/AuthorizationCommands";
import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";
import { AuthorizationTokenType } from "@common/data/entities/authorization/AuthorizationToken";
import { useNetworkStore } from "@common/data/stores/NetworkStore";

import { FrontendComponent } from "@/component/FrontendComponent";
import { getURLQueryParam } from "@common/utils/URLUtils";
import { data } from "autoprefixer";

/**
 * Base class for all authorization strategies.
 */
export abstract class AuthorizationStrategy {
    protected readonly _component: FrontendComponent;

    private readonly _strategy: string;

    private readonly _embedded: boolean;

    protected constructor(comp: FrontendComponent, strategy: string, embedded: boolean = false) {
        this._component = comp;

        this._strategy = strategy;

        this._embedded = embedded;
    }

    /**
     * Requests user authorization.
     *
     * @param authState - The current authorization state.
     */
    public requestAuthorization(authState: AuthorizationState): Promise<AuthorizationState> {
        const promise = new Promise<AuthorizationState>(async (resolve, reject) => {
            // Authorization only needs to be requested if not done yet
            if (authState == AuthorizationState.Authorized) {
                resolve(AuthorizationState.Authorized);
                return;
            }

            if (getURLQueryParam("auth:action") === "request") {
                const nwStore = useNetworkStore();

                RequestAuthorizationCommand.build(
                    this._component.frontendService.messageBuilder,
                    AuthorizationTokenType.Host,
                    this.strategy,
                    this.getRequestData(),
                )
                    .done((_, success: boolean, msg: string) => {
                        success ? resolve(AuthorizationState.Authorized) : reject(msg);
                    })
                    .failed((_, msg: string) => reject(msg))
                    .emit(nwStore.serverChannel);
            } else {
                this.initiateRequest();
                resolve(AuthorizationState.Pending);
            }
        });
        promise.then(this.finishRequest);
        return promise;
    }

    protected abstract initiateRequest(): void;

    protected abstract getRequestData(): any;

    protected finishRequest(authState: AuthorizationState): void {}

    protected redirect(url: string): void {
        if (url) {
            // Not sure if this will always work with all browsers and web servers
            // Might need to open the URL in a new window
            this._embedded ? window.parent.location.replace(url) : window.location.replace(url);
        }
    }

    /**
     * The strategy identifier.
     */
    public get strategy(): string {
        return this._strategy;
    }
}
