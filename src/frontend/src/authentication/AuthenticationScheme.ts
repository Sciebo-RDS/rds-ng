import { type VueComponent } from "@common/component/WebComponent";

import { Authenticator } from "@/authentication/Authenticator";
import { FrontendComponent } from "@/component/FrontendComponent";

/**
 * Base class for authentication themes.
 */
export abstract class AuthenticationScheme {
    protected readonly _comp: FrontendComponent;

    private readonly _scheme: string;

    private readonly _authComponent: VueComponent;

    protected constructor(comp: FrontendComponent, scheme: string, authComponent: VueComponent) {
        this._comp = comp;

        this._scheme = scheme;

        this._authComponent = authComponent;
    }

    /**
     * Creates a new authenticator.
     */
    public abstract authenticator(...args: any[]): Authenticator;

    /**
     * The scheme identifier.
     */
    public get scheme(): string {
        return this._scheme;
    }

    /**
     * ,The authentication component used during the login process.
     */
    public get authComponent(): VueComponent {
        return this._authComponent;
    }
}
