import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { RevokeAuthorizationAction } from "@/ui/actions/authorization/RevokeAuthorizationAction";
import { editConnectorInstanceDialog } from "@/ui/dialogs/connector/instance/EditConnectorInstanceDialog";
import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";
import { AuthorizationTokenType } from "@common/data/entities/authorization/AuthorizationToken";
import { getConnectorInstanceAuthorizationID } from "@common/data/entities/authorization/AuthorizationTokenUtils";
import { Connector } from "@common/data/entities/connector/Connector";
import { ConnectorInstance, type ConnectorInstanceID } from "@common/data/entities/connector/ConnectorInstance";
import { createAuthorizationStrategyFromConnectorInstance } from "@common/data/entities/connector/ConnectorInstanceUtils";
import { findConnectorByID } from "@common/data/entities/connector/ConnectorUtils";
import { AuthorizationRequest } from "@common/integration/authorization/AuthorizationRequest";

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

    function requestInstanceAuthorization(instance: ConnectorInstance, connectors: Connector[]): void {
        if (instance.authorization_state == AuthorizationState.Authorized) {
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
        strategy.initiateAuthorizationRequest(authRequest);
    }

    function revokeInstanceAuthorization(instance: ConnectorInstance, connectors: Connector[]): void {
        if (instance.authorization_state != AuthorizationState.Authorized) {
            return;
        }

        const action = new RevokeAuthorizationAction(comp);
        action.prepare(getConnectorInstanceAuthorizationID(instance), `connector ${instance.name}`);
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
