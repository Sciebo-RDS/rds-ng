import { RequestAuthorizationCommand } from "../../../api/authorization/AuthorizationCommands";
import { WebComponent } from "../../../component/WebComponent";
import { AuthorizationState } from "../../../data/entities/authorization/AuthorizationState";
import { AuthorizationTokenType } from "../../../data/entities/authorization/AuthorizationToken";
import { useNetworkStore } from "../../../data/stores/NetworkStore";
import { Service } from "../../../services/Service";
import { RedirectionTarget } from "../../../utils/HTMLUtils";
import { getURLQueryParam } from "../../../utils/URLUtils";

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
     * Requests user authorization.
     *
     * @param authState - The current authorization state.
     * @param fingerprint - The user's fingerprint.
     */
    public requestAuthorization(authState: AuthorizationState, fingerprint: string): Promise<AuthorizationState> {
        return new Promise<AuthorizationState>(async (resolve, reject) => {
            // Authorization only needs to be requested if not done yet
            if (authState == AuthorizationState.Authorized) {
                resolve(AuthorizationState.Authorized);
                return;
            }

            if (getURLQueryParam("auth:action") === "request") {
                const nwStore = useNetworkStore();

                RequestAuthorizationCommand.build(
                    this._service.messageBuilder,
                    AuthorizationTokenType.Host,
                    this.strategy,
                    this.getRequestData(),
                    this.getFingerprintParam(),
                )
                    .done((_, success: boolean, msg: string) => {
                        success ? resolve(AuthorizationState.Authorized) : reject(msg);

                        if (success) {
                            this.finishRequest();
                        }
                    })
                    .failed((_, msg: string) => reject(msg))
                    .emit(nwStore.serverChannel);
            } else {
                this.initiateRequest(fingerprint);
                resolve(AuthorizationState.Pending);
            }
        });
    }

    protected abstract initiateRequest(fingerprint: string): void;

    protected abstract getRequestData(): any;

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

    private getFingerprintParam(): string {
        const fingerprint = getURLQueryParam("auth:fingerprint");
        if (!fingerprint) {
            throw new Error("No authentication fingerprint provided");
        }
        return fingerprint;
    }

    /**
     * The strategy identifier.
     */
    public get strategy(): string {
        return this._strategy;
    }
}
