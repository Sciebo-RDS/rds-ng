import { Connector } from "@common/data/entities/connector/Connector";
import { ConnectorInstance, type ConnectorInstanceID } from "@common/data/entities/connector/ConnectorInstance";
import { connectorRequiresAuthorization, findConnectorByID } from "@common/data/entities/connector/ConnectorUtils";

import { FrontendComponent } from "@/component/FrontendComponent";
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

    function requestInstanceAuthorization(instance: ConnectorInstance, connectors: Connector[]): void {
        const connector = findConnectorByID(connectors, instance.connector_id);
        if (!connector || !connectorRequiresAuthorization(connector)) {
            return;
        }
        console.log("AYYYY REQUEST");
    }

    function revokeInstanceAuthorization(instance: ConnectorInstance, connectors: Connector[]): void {
        const connector = findConnectorByID(connectors, instance.connector_id);
        if (!connector || !connectorRequiresAuthorization(connector)) {
            return;
        }
        console.log("AYYYY REVOKE");
    }

    return {
        newInstance,
        editInstance,
        deleteInstance,
        requestInstanceAuthorization,
        revokeInstanceAuthorization,
    };
}
