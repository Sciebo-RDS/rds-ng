import { type VueComponent } from "@common/component/WebComponent";
import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";
import { getNonHostTokenTypes } from "@common/data/entities/authorization/AuthorizationToken";
import { isUserTokenValid } from "@common/data/entities/user/UserToken";
import { AuthorizationRequest } from "@common/integration/authorization/AuthorizationRequest";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { Authenticator } from "@/integration/authentication/Authenticator";
import { AuthorizationRequestsHandler } from "@/integration/authorization/AuthorizationRequestsHandler";
import { Authorizer } from "@/integration/authorization/Authorizer";
import { ResourcesBroker } from "@/integration/resources/brokers/ResourcesBroker";
import { useFrontendTools } from "@/ui/tools/FrontendTools";

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
     * Creates a new resources broker.
     */
    public abstract resourcesBroker(...args: any[]): ResourcesBroker;

    /**
     * Checks whether the integration has completed.
     */
    public get isIntegrated(): boolean {
        // The integration is completed when the user has been authenticated, authorized, and a broker has been assigned
        const { userToken, authorizationState, brokerAssigned } = useUserStore();
        return isUserTokenValid(userToken) && authorizationState == AuthorizationState.Authorized && brokerAssigned;
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
     * Called when the app has launched after completed integration.
     *
     * @returns - A promise that can be used to perform tasks after post-initialization.
     */
    public startSession(): Promise<void> {
        const promise = new Promise<void>(async (resolve, reject) => {
            // When the session begins, perform any pending authorizations
            this.handlePendingAuthorizationRequests()
                .then(resolve)
                .catch((error) => reject(`Authorization request failed: ${error}`));
        });
        promise.catch((error) => {
            const { setInitializationMessage } = useFrontendTools(this._component);
            setInitializationMessage(error, true);
        });
        return promise;
    }

    /**
     * Called when the user leaves the main view.
     */
    public endSession(): void {}

    /**
     * The scheme identifier.
     */
    public get scheme(): string {
        return this._scheme;
    }

    /**
     * The integration component used during the login process.
     */
    public get integrationComponent(): VueComponent {
        return this._integrationComponent;
    }

    private handlePendingAuthorizationRequests(): Promise<void> {
        const { setInitializationMessage } = useFrontendTools(this._component);

        // We only deal with non-host authorizations here
        if (AuthorizationRequest.requestIssued(getNonHostTokenTypes())) {
            setInitializationMessage("Performing authorization...");

            const handler = new AuthorizationRequestsHandler(this._component, this._component.frontendService);
            return handler.handlePendingRequests();
        } else {
            return new Promise<void>(async (resolve, reject) => {
                resolve();
            });
        }
    }
}
