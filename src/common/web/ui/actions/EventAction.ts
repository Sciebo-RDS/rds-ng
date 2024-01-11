import { EventComposer } from "../../core/messaging/composers/EventComposer";
import { Event } from "../../core/messaging/Event";
import { Action } from "./Action";
import { ActionState } from "./ActionBase";

/**
 * Actions specific to ``Event``.
 */
export abstract class EventAction<EventType extends Event, CompType extends EventComposer<EventType>> extends Action<EventType, CompType> {
    protected postExecution(): void {
        this.setState(ActionState.Done);

        super.postExecution();
    }
}
