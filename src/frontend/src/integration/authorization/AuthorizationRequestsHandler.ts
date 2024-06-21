import { WebComponent } from "@common/component/WebComponent";
import logging from "@common/core/logging/Logging";
import { AuthorizationTokenType } from "@common/data/entities/authorization/AuthorizationToken";
import { createAuthorizationStrategyFromConnectorInstance } from "@common/data/entities/connector/ConnectorInstanceUtils";
import { findConnectorInstanceByID } from "@common/data/entities/connector/ConnectorUtils";
import { AuthorizationRequest } from "@common/integration/authorization/AuthorizationRequest";
import { AuthorizationStrategy } from "@common/integration/authorization/strategies/AuthorizationStrategy";
import { Service } from "@common/services/Service";

import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useUserStore } from "@/data/stores/UserStore";

/**
 * Class to handle pending authorization requests (except for host authorization).
 */
export class AuthorizationRequestsHandler {
    private readonly _component: WebComponent;
    private readonly _service: Service;

    /**
     * @param comp - The global component.
     * @param svc - The service used for message sending.
     */
    public constructor(comp: WebComponent, svc: Service) {
        this._component = comp;
        this._service = svc;
    }

    public handlePendingRequests(): Promise<void> {
        return new Promise<void>(async (resolve, reject) => {
            // Only one request can be pending, so fetch it from the URL
            const authRequest = AuthorizationRequest.fromURLParameters();
            this.handleRequest(authRequest, resolve, reject);
        });
    }

    private handleRequest(authRequest: AuthorizationRequest, resolve: () => void, reject: (msg: string) => void): void {
        const strategy = this.createAuthStrategy(authRequest);
        if (strategy) {
            strategy
                .executeAuthorizationRequest(authRequest)
                .then(() => {
                    logging.info("Authorization request succeeded", "authorization", this.getLoggingParams(authRequest));
                    resolve();
                })
                .catch((error) => {
                    logging.error("Authorization request failed", "authorization", { ...this.getLoggingParams(authRequest), error: error });
                    reject(`Authorization request failed: ${error}`);
                });
        } else {
            logging.warning("Unable to process authorization request", "authorization", this.getLoggingParams(authRequest));
            reject("Unable to process authorization request");
        }
    }

    private createAuthStrategy(authRequest: AuthorizationRequest): AuthorizationStrategy | undefined {
        // Each authorization type needs to be handled differently to get the proper strategy
        switch (authRequest.payload.auth_type) {
            case AuthorizationTokenType.Connector:
                return this.createAuthStrategyForConnectorInstance(authRequest);

            default:
                return undefined;
        }
    }

    private createAuthStrategyForConnectorInstance(authRequest: AuthorizationRequest): AuthorizationStrategy | undefined {
        const userStore = useUserStore();
        const conStore = useConnectorsStore();

        const instance = findConnectorInstanceByID(userStore.userSettings.connector_instances, authRequest.payload.auth_issuer);
        if (!instance) {
            return undefined;
        }
        return createAuthorizationStrategyFromConnectorInstance(this._component, this._service, instance, conStore.connectors);
    }

    private getLoggingParams(authRequest: AuthorizationRequest): Record<string, any> {
        return {
            id: authRequest.payload.auth_id,
            type: authRequest.payload.auth_type,
            issuer: authRequest.payload.auth_issuer,
        };
    }
}
