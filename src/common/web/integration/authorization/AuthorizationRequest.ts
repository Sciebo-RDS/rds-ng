import { AuthorizationTokenType } from "../../data/entities/authorization/AuthorizationToken";
import { getURLQueryParam } from "../../utils/URLUtils";

/**
 * The payload that is sent with authorization requests.
 */
export interface AuthorizationRequestPayload {
    auth_id: string;
    auth_type: AuthorizationTokenType;
    auth_issuer: string;

    fingerprint: string;
}

/**
 * Helper class to deal with authorization requests and their payload.
 */
export class AuthorizationRequest {
    private _payload: AuthorizationRequestPayload;

    private constructor() {
        this._payload = {
            auth_id: "",
            auth_type: AuthorizationTokenType.Invalid,
            auth_issuer: "",
            fingerprint: "",
        } as AuthorizationRequestPayload;
    }

    /**
     * Creates a new authorization request based on values.
     *
     * @param authID - The authorization ID.
     * @param authType - The authorization type.
     * @param authIssuer - The issuer of the authorization.
     * @param fingerprint - The user's fingerprint.
     */
    public static fromValues(authID: string, authType: AuthorizationTokenType, authIssuer: string, fingerprint: string): AuthorizationRequest {
        const request = new AuthorizationRequest();
        request._payload = {
            auth_id: authID,
            auth_type: authType,
            auth_issuer: authIssuer,
            fingerprint: fingerprint,
        } as AuthorizationRequestPayload;
        return request;
    }

    public static fromURLParam() {
        const request = new AuthorizationRequest();
        request.payloadFromURLParam();
        return request;
    }

    /**
     * Whether an authorization request has been issued and should be handled now.
     *
     * @param authTypes - The authorization types to check for.
     */
    public static requestIssued(authTypes: AuthorizationTokenType[] = []): boolean {
        if (getURLQueryParam("auth:action") === "request") {
            try {
                const authRequest = AuthorizationRequest.fromURLParam();
                if (authTypes.length == 0 || authTypes.includes(authRequest.payload.auth_type)) {
                    return true;
                }
            } catch (e) {}
        }
        return false;
    }

    /**
     * Compares this request to another one, throwing an error in case of any mismatch.
     *
     * @param other - The authorization request to compare to.
     */
    public verify(other: AuthorizationRequest): void {
        const checkPayload = (name: string, expected: string, got: string): void => {
            if (expected != got) {
                throw new Error(`Authorization ${name} mismatch: Expected ${expected}, got ${got}`);
            }
        };

        checkPayload("ID", this.payload.auth_id, other.payload.auth_id);
        checkPayload("type", this.payload.auth_type, other.payload.auth_type);
        checkPayload("issuer", this.payload.auth_issuer, other.payload.auth_issuer);
    }

    /**
     * The request payload.
     */
    public get payload(): AuthorizationRequestPayload {
        return this._payload;
    }

    /**
     * The request payload, encoded as a base64 string.
     */
    public get encodedPayload(): string {
        return this.encodeRequestPayload();
    }

    private payloadFromURLParam(): void {
        this._payload = this.decodeRequestPayload();
    }

    private encodeRequestPayload(): string {
        return btoa(JSON.stringify(this._payload));
    }

    private decodeRequestPayload(): AuthorizationRequestPayload {
        const payload = getURLQueryParam("auth:payload");
        if (!payload) {
            throw new Error("No authentication payload provided");
        }
        return JSON.parse(atob(payload)) as AuthorizationRequestPayload;
    }
}
