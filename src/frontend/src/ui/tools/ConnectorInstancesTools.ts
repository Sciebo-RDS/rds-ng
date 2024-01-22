import { Connector } from "@common/data/entities/connector/Connector";
import { ConnectorInstance, type ConnectorInstanceID } from "@common/data/entities/connector/ConnectorInstance";

import { FrontendComponent } from "@/component/FrontendComponent";

export function useConnectorInstancesTools(comp: FrontendComponent) {
    function createInstance(instances: ConnectorInstance[], connector: Connector): ConnectorInstanceID {
        // TODO
        const instanceID = (instances.length ? instances[instances.length - 1].instance_id + 1 : 1) as ConnectorInstanceID;
        instances.push(
            new ConnectorInstance(instanceID, connector.connector_id, "I am new!", "And not unique...")
        );
        return instanceID;
    }

    function editInstance(instance: ConnectorInstance): void {
        // TODO
        console.log("Edit " + instance.name);
    }

    function deleteInstance(instances: ConnectorInstance[], instance: ConnectorInstance): void {
        const index = instances.indexOf(instance);
        if (index != -1) {
            instances.splice(index, 1);
        }
    }

    return {
        createInstance,
        editInstance,
        deleteInstance
    };
}
