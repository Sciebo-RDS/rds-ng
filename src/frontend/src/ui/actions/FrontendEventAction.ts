import { EventComposer } from "@common/core/messaging/composers/EventComposer";
import { Event } from "@common/core/messaging/Event";
import { EventAction } from "@common/ui/actions/EventAction";

import { type FrontendComponent } from "@/component/FrontendComponent";

/**
 * Event actions specific to the frontend.
 */
export abstract class FrontendEventAction<EventType extends Event, CompType extends EventComposer<EventType>> extends EventAction<EventType, CompType> {
    /**
     * @param comp - The main frontend component.
     * @param suppressDefaultNotifiers - Suppress default notifiers.
     */
    public constructor(comp: FrontendComponent, suppressDefaultNotifiers: boolean = false) {
        super(comp.frontendService, suppressDefaultNotifiers);
    }
}
