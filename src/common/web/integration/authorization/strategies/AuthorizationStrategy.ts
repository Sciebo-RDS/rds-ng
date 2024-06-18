import { RequestAuthorizationCommand } from "../../../api/authorization/AuthorizationCommands";
import { WebComponent } from "../../../component/WebComponent";
import { AuthorizationState } from "../../../data/entities/authorization/AuthorizationState";
import { AuthorizationTokenType } from "../../../data/entities/authorization/AuthorizationToken";
import { useNetworkStore } from "../../../data/stores/NetworkStore";
import { Service } from "../../../services/Service";
import { RedirectionTarget } from "../../../utils/HTMLUtils";
import { getURLQueryParam } from "../../../utils/URLUtils";

/**
 * The payload that is sent with authorization requests.
 */
export interface AuthorizationStrategyPayload {
    auth_id: string;
    auth_type: AuthorizationTokenType;
    auth_issuer: string;

    fingerprint: string;
}

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
     * Whether an authorization request has been issued and should be handled now.
     *
     * @param authTypes - The authorization type(s).
     */
    public static authorizationRequestIssued(authTypes: AuthorizationTokenType | AuthorizationTokenType[]): boolean {
        if (getURLQueryParam("auth:action") === "request") {
            try {
                const payload = AuthorizationStrategy.decodeRequestPayload();
                if ((Array.isArray(authTypes) && authTypes.includes(payload.auth_type)) || (!Array.isArray(authTypes) && payload.auth_type == authTypes)) {
                    return true;
                }
            } catch (e) {}
        }
        return false;
    }

    /**
     * Initiates an authorization request.
     *
     * @param authID - The authorization ID.
     * @param authType - The authorization type.
     * @param authIssuer - The issuer of the authorization.
     * @param fingerprint - The user's fingerprint.
     */
    public initiateAuthorizationRequest(authID: string, authType: AuthorizationTokenType, authIssuer: string, fingerprint: string): void {
        this.initiateRequest(AuthorizationStrategy.encodeRequestPayload(authID, authType, authIssuer, fingerprint));
    }

    /**
     * Executes an authorization requests (requires a preceding initiation).
     *
     * @param authID - The authorization ID.
     * @param authType - The authorization type.
     * @param authIssuer - The issuer of the authorization.
     */
    public executeAuthorizationRequest(authID: string, authType: AuthorizationTokenType, authIssuer: string): Promise<AuthorizationState> {
        return new Promise<AuthorizationState>(async (resolve, reject) => {
            const nwStore = useNetworkStore();
            const payload = AuthorizationStrategy.decodeRequestPayload();

            // Make sure that we're dealing with the correct request
            const checkPayload = (name: string, expected: string, got: string): boolean => {
                if (expected != got) {
                    reject(`Authorization ${name} mismatch: Expected ${expected}, got ${got}`);
                    return false;
                }
                return true;
            };
            if (!checkPayload("ID", authID, payload.auth_id)) {
                return;
            }
            if (!checkPayload("type", authType, payload.auth_type)) {
                return;
            }
            if (!checkPayload("issuer", authIssuer, payload.auth_issuer)) {
                return;
            }

            RequestAuthorizationCommand.build(this._service.messageBuilder, authID, this.strategy, this.getRequestData(), payload.fingerprint)
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
     * @param authID - The authorization ID.
     * @param authType - The authorization type.
     * @param authIssuer - The issuer of the authorization.
     * @param authState - The current authorization state.
     * @param fingerprint - The user's fingerprint.
     */
    public requestAuthorization(
        authID: string,
        authType: AuthorizationTokenType,
        authIssuer: string,
        authState: AuthorizationState,
        fingerprint: string,
    ): Promise<AuthorizationState> {
        if (authState == AuthorizationState.Authorized) {
            return new Promise<AuthorizationState>(async (resolve, reject) => {
                resolve(AuthorizationState.Authorized);
            });
        }

        if (AuthorizationStrategy.authorizationRequestIssued(authType)) {
            return this.executeAuthorizationRequest(authID, authType, authIssuer);
        } else {
            return new Promise<AuthorizationState>(async (resolve, reject) => {
                this.initiateAuthorizationRequest(authID, authType, authIssuer, fingerprint);
                resolve(AuthorizationState.Pending);
            });
        }
    }

    protected abstract initiateRequest(payload: string): void;

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

    private static getPayloadParam(): string {
        const payload = getURLQueryParam("auth:payload");
        if (!payload) {
            throw new Error("No authentication payload provided");
        }
        return payload;
    }

    private static encodeRequestPayload(authID: string, authType: AuthorizationTokenType, authIssuer: string, fingerprint: string): string {
        const payload = {
            auth_id: authID,
            auth_type: authType,
            auth_issuer: authIssuer,
            fingerprint: fingerprint,
        } as AuthorizationStrategyPayload;

        return btoa(JSON.stringify(payload));
    }

    private static decodeRequestPayload(): AuthorizationStrategyPayload {
        return JSON.parse(atob(AuthorizationStrategy.getPayloadParam())) as AuthorizationStrategyPayload;
    }

    /**
     * The strategy identifier.
     */
    public get strategy(): string {
        return this._strategy;
    }
}
