import { RequestAuthorizationCommand } from "../../../api/authorization/AuthorizationCommands";
import { WebComponent } from "../../../component/WebComponent";
import { AuthorizationState } from "../../../data/entities/authorization/AuthorizationState";
import { useNetworkStore } from "../../../data/stores/NetworkStore";
import { Service } from "../../../services/Service";
import { RedirectionTarget } from "../../../utils/HTMLUtils";
import { AuthorizationRequest } from "../AuthorizationRequest";

/**
 * Base class for all authorization strategies.
 */
export abstract class AuthorizationStrategy {
    protected readonly _component: WebComponent;
    protected readonly _service: Service;

    private readonly _strategy: string;

    private readonly _redirectionTarget: RedirectionTarget;

    protected constructor(comp: WebComponent, svc: Service, strategy: string, redirectionTarget: RedirectionTarget = RedirectionTarget.Same) {
        this._component = comp;
        this._service = svc;

        this._strategy = strategy;

        this._redirectionTarget = redirectionTarget;
    }

    /**
     * Initiates an authorization request.
     *
     * @param authRequest - The authorization request.
     */
    public initiateAuthorizationRequest(authRequest: AuthorizationRequest): void {
        this.initiateRequest(authRequest);
    }

    /**
     * Executes an authorization requests (requires a preceding initiation).
     *
     * @param authRequest - The authorization request.
     */
    public executeAuthorizationRequest(authRequest: AuthorizationRequest): Promise<AuthorizationState> {
        return new Promise<AuthorizationState>(async (resolve, reject) => {
            const nwStore = useNetworkStore();

            // Make sure that we're dealing with the correct request
            const urlRequest = AuthorizationRequest.fromURLParameters();
            try {
                authRequest.verify(urlRequest);
            } catch (exc) {
                reject(exc);
                return false;
            }

            RequestAuthorizationCommand.build(this._service.messageBuilder, authRequest.payload, this.strategy, this.getRequestData(authRequest))
                .done((_, success: boolean, msg: string) => {
                    success ? resolve(AuthorizationState.Authorized) : reject(msg);

                    if (success) {
                        this.finishRequest();
                    }
                })
                .failed((_, msg: string) => reject(msg))
                .emit(nwStore.serverChannel);
        });
    }

    /**
     * Requests user authorization, handling all steps automatically.
     *
     * @param authState - The current authorization state.
     * @param authRequest - The authorization request.
     */
    public requestAuthorization(authState: AuthorizationState, authRequest: AuthorizationRequest): Promise<AuthorizationState> {
        if (authState == AuthorizationState.Authorized) {
            return new Promise<AuthorizationState>(async (resolve, _) => {
                resolve(AuthorizationState.Authorized);
            });
        }

        if (AuthorizationRequest.requestIssued([authRequest.payload.auth_type])) {
            return this.executeAuthorizationRequest(authRequest);
        } else {
            return new Promise<AuthorizationState>(async (resolve, _) => {
                this.initiateAuthorizationRequest(authRequest);
                resolve(AuthorizationState.Pending);
            });
        }
    }

    protected abstract initiateRequest(authRequest: AuthorizationRequest): void;

    protected abstract getRequestData(authRequest: AuthorizationRequest): any;

    protected finishRequest(): void {}

    protected redirect(url: string): void {
        if (url) {
            // Not sure if this will always work with all browsers and web servers
            // Might need to open the URL in a new window
            switch (this._redirectionTarget) {
                case RedirectionTarget.Same:
                    window.location.replace(url);
                    break;

                case RedirectionTarget.Parent:
                    window.parent.location.replace(url);
                    break;

                case RedirectionTarget.Blank:
                    // @ts-ignore
                    window.open(url, "_blank").focus();
                    break;
            }
        }
    }

    /**
     * The strategy identifier.
     */
    public get strategy(): string {
        return this._strategy;
    }
}
