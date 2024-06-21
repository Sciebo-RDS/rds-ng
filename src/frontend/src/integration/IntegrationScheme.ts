import { type VueComponent } from "@common/component/WebComponent";
import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";
import { getNonHostTokenTypes } from "@common/data/entities/authorization/AuthorizationToken";
import { isUserTokenValid } from "@common/data/entities/user/UserToken";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { Authenticator } from "@/integration/authentication/Authenticator";
import { AuthorizationRequestsHandler } from "@/integration/authorization/AuthorizationRequestsHandler";
import { Authorizer } from "@/integration/authorization/Authorizer";
import { ResourcesBroker } from "@/integration/resources/brokers/ResourcesBroker";
import { AuthorizationRequest } from "@common/integration/authorization/AuthorizationRequest";

/**
 * Callback type used during session startup.
 */
export type StartSessionStatusCallback = (status: string) => void;

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
     * @param reportStatus - A callback that receives the current status of the startup phase.
     *
     * @returns - A promise that can be used to perform tasks after post-initialization.
     */
    public startSession(reportStatus: StartSessionStatusCallback | undefined = undefined): Promise<void> {
        if (!reportStatus) {
            reportStatus = (_: string) => {};
        }

        return new Promise<void>(async (resolve, reject) => {
            // When the session begins, perform any pending authorizations (which are not for the host integration)
            this.handlePendingAuthorizationRequests(reportStatus).then(resolve).catch(reject);
        });
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

    private handlePendingAuthorizationRequests(reportStatus: StartSessionStatusCallback): Promise<void> {
        if (AuthorizationRequest.requestIssued(getNonHostTokenTypes())) {
            reportStatus("Performing authorization...");

            const handler = new AuthorizationRequestsHandler(this._component, this._component.frontendService);
            return handler.handlePendingRequests();
        } else {
            return new Promise<void>(async (resolve, _) => {
                resolve();
            });
        }
    }
}
