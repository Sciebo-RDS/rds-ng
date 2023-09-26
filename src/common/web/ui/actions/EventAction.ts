import { EventComposer } from "../../core/messaging/composers/EventComposer";
import { Event } from "../../core/messaging/Event";
import { Action } from "./Action";

export type EventActionCallback<EventType extends Event> = (composer: EventComposer<EventType>) => void;

/**
 * Event actions.
 */
export class EventAction<EventType extends Event> extends Action<EventType, EventComposer<EventType>> {
}
