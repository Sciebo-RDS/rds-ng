import { FrontendComponent } from "@/component/FrontendComponent";
import { ResourcesBroker } from "@/integration/broker/ResourcesBroker";
import { type HostResources } from "@/integration/HostTypes";

/**
 * Resources broker for host integration.
 */
export class HostResourcesBroker extends ResourcesBroker {
    public constructor(comp: FrontendComponent, hostResources: HostResources) {
        super(comp, hostResources);
    }

    public assign(): void {
        this.assignBrokerWithHostResources();
    }
}
