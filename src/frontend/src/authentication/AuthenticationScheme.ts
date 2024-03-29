import { type VueComponent } from "@common/component/WebComponent";

import { Authenticator } from "@/authentication/Authenticator";
import { isUserTokenValid } from "@/authentication/UserToken";
import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";

/**
 * Base class for authentication themes.
 */
export abstract class AuthenticationScheme {
    protected readonly _component: FrontendComponent;

    private readonly _scheme: string;

    private readonly _authComponent: VueComponent;

    protected constructor(comp: FrontendComponent, scheme: string, authComponent: VueComponent) {
        this._component = comp;

        this._scheme = scheme;

        this._authComponent = authComponent;
    }

    /**
     * Creates a new authenticator.
     */
    public abstract authenticator(...args: any[]): Authenticator;

    /**
     * Checks whether the user is authenticated.
     */
    public get isAuthenticated(): boolean {
        const { userToken } = useUserStore();
        return isUserTokenValid(userToken);
    }

    /**
     * Called when the user enters the app.
     */
    public enter(): void {
    }

    /**
     * Called when the user leaves the app (e.g., by closing or refreshing it).
     */
    public leave(): void {
    }

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
