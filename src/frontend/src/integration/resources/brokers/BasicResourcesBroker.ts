import { FrontendComponent } from "@/component/FrontendComponent";
import { ResourcesBroker } from "@/integration/resources/brokers/ResourcesBroker";
import { type HostResources } from "@/integration/HostTypes";

/**
 * Resources broker for basic integration.
 */
export class BasicResourcesBroker extends ResourcesBroker {
    public constructor(comp: FrontendComponent) {
        super(comp, { broker: "filesystem", config: { root: "" } } as HostResources);
    }

    public assign(): void {
        this.assignBrokerWithHostResources();
    }
}
