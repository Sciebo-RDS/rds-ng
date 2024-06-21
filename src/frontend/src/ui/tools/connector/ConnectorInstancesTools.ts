import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";
import { AuthorizationTokenType } from "@common/data/entities/authorization/AuthorizationToken";
import { getConnectorInstanceAuthorizationID } from "@common/data/entities/authorization/AuthorizationTokenUtils";
import { Connector } from "@common/data/entities/connector/Connector";
import { ConnectorInstance, type ConnectorInstanceID } from "@common/data/entities/connector/ConnectorInstance";
import { connectorInstanceIsAuthorized, createAuthorizationStrategyFromConnectorInstance } from "@common/data/entities/connector/ConnectorInstanceUtils";
import { findConnectorByID } from "@common/data/entities/connector/ConnectorUtils";
import { AuthorizationRequest } from "@common/integration/authorization/AuthorizationRequest";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { ListUserAuthorizationsAction } from "@/ui/actions/authorization/ListUserAuthorizationsAction";
import { RevokeAuthorizationAction } from "@/ui/actions/authorization/RevokeAuthorizationAction";
import { editConnectorInstanceDialog } from "@/ui/dialogs/connector/instance/EditConnectorInstanceDialog";

export function useConnectorInstancesTools(comp: FrontendComponent) {
    async function newInstance(instances: ConnectorInstance[], connector: Connector): Promise<ConnectorInstance> {
        return editConnectorInstanceDialog(comp, undefined, connector).then((data) => {
            const instance = new ConnectorInstance(crypto.randomUUID() as ConnectorInstanceID, connector.connector_id, data.name, data.description);
            instances.push(instance);
            return instance;
        });
    }

    async function editInstance(instances: ConnectorInstance[], instance: ConnectorInstance, connector?: Connector): Promise<ConnectorInstance> {
        return editConnectorInstanceDialog(comp, instance, connector).then((data) => {
            const editedInstance = new ConnectorInstance(instance.instance_id, instance.connector_id, data.name, data.description);
            const index = instances.indexOf(instance);
            if (index == -1) {
                instances.push(editedInstance);
            } else {
                instances[index] = editedInstance;
            }
            return editedInstance;
        });
    }

    function deleteInstance(instances: ConnectorInstance[], instance: ConnectorInstance): void {
        const index = instances.indexOf(instance);
        if (index != -1) {
            instances.splice(index, 1);
        }
    }

    function requestInstanceAuthorization(instance: ConnectorInstance, connectors: Connector[], authorizations: string[]): void {
        if (connectorInstanceIsAuthorized(instance, authorizations)) {
            return;
        }

        const connector = findConnectorByID(connectors, instance.connector_id);
        if (!connector) {
            return;
        }
        const strategy = createAuthorizationStrategyFromConnectorInstance(comp, comp.frontendService, instance, connectors);
        if (!strategy) {
            return;
        }

        const { userFingerprint } = useUserStore();
        const authRequest = AuthorizationRequest.fromValues(
            getConnectorInstanceAuthorizationID(instance),
            AuthorizationTokenType.Connector,
            instance.instance_id,
            connector.connector_id,
            userFingerprint,
        );
        strategy.requestCompleted(() => {
            // Once the request has completed, fetch all user authorizations
            const action = new ListUserAuthorizationsAction(comp);
            action.prepare();
            action.execute();
        });
        strategy.initiateAuthorizationRequest(authRequest);
    }

    function revokeInstanceAuthorization(instance: ConnectorInstance, updateAuthState: boolean = true): void {
        const action = new RevokeAuthorizationAction(comp);
        action.prepare(getConnectorInstanceAuthorizationID(instance), `connector ${instance.name}`).done((_, success, msg) => {
            if (success && updateAuthState) {
                // @ts-ignore
                instance.authorization_state = AuthorizationState.NotAuthorized;
            }
        });
        action.execute();
    }

    return {
        newInstance,
        editInstance,
        deleteInstance,
        requestInstanceAuthorization,
        revokeInstanceAuthorization,
    };
}
