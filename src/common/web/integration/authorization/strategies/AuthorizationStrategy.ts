import { RequestAuthorizationCommand } from "../../../api/authorization/AuthorizationCommands";
import { WebComponent } from "../../../component/WebComponent";
import { AuthorizationState } from "../../../data/entities/authorization/AuthorizationState";
import { useNetworkStore } from "../../../data/stores/NetworkStore";
import { Service } from "../../../services/Service";
import { ExecutionCallbacks } from "../../../utils/ExecutionCallbacks";
import { RedirectionTarget } from "../../../utils/HTMLUtils";
import { AuthorizationRequest } from "../AuthorizationRequest";

/**
 * Notification type of finished requests callbacks.
 */
export type AuthorizationRequestCallback = () => void;

/**
 * Base class for all authorization strategies.
 */
export abstract class AuthorizationStrategy {
    protected readonly _component: WebComponent;
    protected readonly _service: Service;

    protected readonly _redirectionTarget: RedirectionTarget;

    private readonly _strategy: string;

    private readonly _executionCallbacks = new ExecutionCallbacks<AuthorizationRequestCallback, AuthorizationRequestCallback>();

    protected constructor(comp: WebComponent, svc: Service, strategy: string, redirectionTarget: RedirectionTarget = RedirectionTarget.Current) {
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

    /**
     * Adds a callback for completed requests.
     *
     * @param cb - The callback to add.
     */
    public requestCompleted(cb: AuthorizationRequestCallback): this {
        this._executionCallbacks.done(cb);
        return this;
    }

    protected abstract initiateRequest(authRequest: AuthorizationRequest): void;

    protected abstract getRequestData(authRequest: AuthorizationRequest): any;

    protected finishRequest(): void {}

    protected redirect(url: string): void {
        if (url) {
            // Not sure if this will always work with all browsers and web servers
            // Might need to open the URL in a new window
            switch (this._redirectionTarget) {
                case RedirectionTarget.Current:
                    this.handleRequestCompletion();

                    // Even if there's no parent, this will work
                    window.parent.location.replace(url);
                    break;

                case RedirectionTarget.Blank:
                    const popupWindow = window.open(url, "_blank");
                    if (popupWindow) {
                        // Get notified when the popup window has closed
                        const timer = setInterval(() => {
                            if (popupWindow.closed) {
                                this.handleRequestCompletion();
                                clearInterval(timer);
                            }
                        }, 100);

                        popupWindow.focus();
                    }
                    break;
            }
        }
    }

    private handleRequestCompletion(): void {
        // Give the system some time to get up again
        setTimeout(() => this._executionCallbacks.invokeDoneCallbacks(), 250);
    }

    /**
     * The strategy identifier.
     */
    public get strategy(): string {
        return this._strategy;
    }
}
