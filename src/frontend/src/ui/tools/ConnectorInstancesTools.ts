import { Connector } from "@common/data/entities/connector/Connector";
import { ConnectorInstance, type ConnectorInstanceID } from "@common/data/entities/connector/ConnectorInstance";

import { FrontendComponent } from "@/component/FrontendComponent";
import { editConnectorInstanceDialog } from "@/ui/dialogs/connector/EditConnectorInstanceDialog";

export function useConnectorInstancesTools(comp: FrontendComponent) {
    function newInstance(instances: ConnectorInstance[], connector: Connector): Promise<ConnectorInstance> {
        return editConnectorInstanceDialog(comp, undefined, connector).then((data) => {
            // TODO
            const instanceID = (instances.length ? instances[instances.length - 1].instance_id + 1 : 1) as ConnectorInstanceID;
            const instance = new ConnectorInstance(instanceID, connector.connector_id, data.name, data.description);
            instances.push(instance);
            return instance;
        });
    }

    function editInstance(instance: ConnectorInstance, connector?: Connector): Promise<ConnectorInstance> {
        return editConnectorInstanceDialog(comp, instance, connector).then((data) => {
            instance.name = data.name;
            instance.description = data.description;
            return instance;
        });
    }

    function deleteInstance(instances: ConnectorInstance[], instance: ConnectorInstance): void {
        const index = instances.indexOf(instance);
        if (index != -1) {
            instances.splice(index, 1);
        }
    }

    return {
        newInstance,
        editInstance,
        deleteInstance
    };
}
