import { RequestAuthorizationCommand } from "../../../api/authorization/AuthorizationCommands";
import { WebComponent } from "../../../component/WebComponent";
import { AuthorizationState } from "../../../data/entities/authorization/AuthorizationState";
import { AuthorizationTokenType } from "../../../data/entities/authorization/AuthorizationToken";
import { useNetworkStore } from "../../../data/stores/NetworkStore";
import { Service } from "../../../services/Service";
import { getURLQueryParam } from "../../../utils/URLUtils";

/**
 * Data composed for an authorization request.
 */
export interface AuthorizationRequestData {
    data: any;

    fingerprint: string;
}

/**
 * Base class for all authorization strategies.
 */
export abstract class AuthorizationStrategy {
    protected readonly _component: WebComponent;
    protected readonly _service: Service;

    private readonly _strategy: string;

    private readonly _embedded: boolean;

    protected constructor(comp: WebComponent, svc: Service, strategy: string, embedded: boolean = false) {
        this._component = comp;
        this._service = svc;

        this._strategy = strategy;

        this._embedded = embedded;
    }

    /**
     * Requests user authorization.
     *
     * @param authState - The current authorization state.
     * @param fingerprint - The user's fingerprint.
     */
    public requestAuthorization(authState: AuthorizationState, fingerprint: string): Promise<AuthorizationState> {
        const promise = new Promise<AuthorizationState>(async (resolve, reject) => {
            // Authorization only needs to be requested if not done yet
            if (authState == AuthorizationState.Authorized) {
                resolve(AuthorizationState.Authorized);
                return;
            }

            if (getURLQueryParam("auth:action") === "request") {
                const nwStore = useNetworkStore();

                const reqData = this.getRequestData();
                RequestAuthorizationCommand.build(this._service.messageBuilder, AuthorizationTokenType.Host, this.strategy, reqData.data, reqData.fingerprint)
                    .done((_, success: boolean, msg: string) => {
                        success ? resolve(AuthorizationState.Authorized) : reject(msg);
                    })
                    .failed((_, msg: string) => reject(msg))
                    .emit(nwStore.serverChannel);
            } else {
                this.initiateRequest(fingerprint);
                resolve(AuthorizationState.Pending);
            }
        });
        promise.then(this.finishRequest);
        return promise;
    }

    protected abstract initiateRequest(fingerprint: string): void;

    protected abstract getRequestData(): AuthorizationRequestData;

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
