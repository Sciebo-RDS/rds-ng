import { storeToRefs } from "pinia";

import { AssignResourcesBrokerCommand, AssignResourcesBrokerReply } from "@common/api/resource/ResourceCommands";
import { useNetworkStore } from "@common/data/stores/NetworkStore";
import { ExecutionCallbacks } from "@common/utils/ExecutionCallbacks";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { type HostResources } from "@/integration/HostTypes";
import { IntegrationBase } from "@/integration/IntegrationBase";

export type ResourcesBrokerDoneCallback = () => void;
export type ResourcesBrokerFailCallback = (msg: string) => void;

/**
 * Base resources broker.
 */
export abstract class ResourcesBroker extends IntegrationBase {
    protected readonly _hostResources: HostResources;

    protected readonly _callbacks = new ExecutionCallbacks<ResourcesBrokerDoneCallback, ResourcesBrokerFailCallback>();

    protected constructor(comp: FrontendComponent, hostResources: HostResources) {
        super(comp);

        this._hostResources = hostResources;
    }

    /**
     * Assigns a broker using the provided host resources.
     */
    public abstract assign(): void;

    /**
     * Adds a *Done* callback.
     *
     * @param cb - The callback to add.
     */
    public done(cb: ResourcesBrokerDoneCallback): ResourcesBroker {
        this._callbacks.done(cb);
        return this;
    }

    /**
     * Adds a *Fail* callback.
     *
     * @param cb - The callback to add.
     */
    public failed(cb: ResourcesBrokerFailCallback): ResourcesBroker {
        this._callbacks.failed(cb);
        return this;
    }

    protected assignBrokerWithHostResources(): void {
        const nwStore = useNetworkStore();

        AssignResourcesBrokerCommand.build(this._component.frontendService.messageBuilder, this._hostResources.broker, this._hostResources.config)
            .done((reply: AssignResourcesBrokerReply, success, msg) => {
                if (success) {
                    const userStore = useUserStore();
                    const { brokerAssigned } = storeToRefs(userStore);

                    brokerAssigned.value = true;

                    this._callbacks.invokeDoneCallbacks();
                } else {
                    this._callbacks.invokeFailCallbacks(msg);
                }
            })
            .failed((_, msg: string) => {
                this._callbacks.invokeFailCallbacks(msg);
            })
            .emit(nwStore.serverChannel);
    }
}
