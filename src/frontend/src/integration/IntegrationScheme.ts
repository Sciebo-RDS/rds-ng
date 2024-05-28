import { isUserTokenValid } from "@common/data/entities/user/UserToken";
import { type VueComponent } from "@common/component/WebComponent";

import { FrontendComponent } from "@/component/FrontendComponent";
import { Authenticator } from "@/integration/auth/Authenticator";
import { Authorizer } from "@/integration/auth/Authorizer";
import { useUserStore } from "@/data/stores/UserStore";

/**
 * Base class for integration schemes.
 */
export abstract class IntegrationScheme {
    protected readonly _component: FrontendComponent;

    private readonly _scheme: string;

    private readonly _integrationComponent: VueComponent;

    protected constructor(comp: FrontendComponent, scheme: string, integrationComponent: VueComponent) {
        this._component = comp;

        this._scheme = scheme;

        this._integrationComponent = integrationComponent;
    }

    /**
     * Creates a new authenticator.
     */
    public abstract authenticator(...args: any[]): Authenticator;

    /**
     * Creates a new authorizer.
     */
    public abstract authorizer(...args: any[]): Authorizer;

    /**
     * Checks whether the integration has completed.
     */
    public get isIntegrated(): boolean {
        const { userToken, isAuthorized } = useUserStore();
        return isUserTokenValid(userToken) && isAuthorized;
    }

    /**
     * Called when the user enters the app.
     */
    public enter(): void {}

    /**
     * Called when the user leaves the app (e.g., by closing or refreshing it).
     */
    public leave(): void {}

    /**
     * The scheme identifier.
     */
    public get scheme(): string {
        return this._scheme;
    }

    /**
     * ,The integration component used during the login process.
     */
    public get integrationComponent(): VueComponent {
        return this._integrationComponent;
    }
}
