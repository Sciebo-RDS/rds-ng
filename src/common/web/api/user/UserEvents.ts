import { Type } from "class-transformer";

import { EventComposer } from "../../core/messaging/composers/EventComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Event } from "../../core/messaging/Event";
import { Message } from "../../core/messaging/Message";

/**
 * Event sent when the user authorizations have changed.
 *
 * @param authorizations - The new list of all granted authorizations.
 */
@Message.define("event/user/authorization/list")
export class UserAuthorizationsListEvent extends Event {
    // @ts-ignore
    @Type(() => String)
    public readonly authorizations: string[] = [];

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, authorizations: string[], chain: Message | null = null): EventComposer<UserAuthorizationsListEvent> {
        return messageBuilder.buildEvent(UserAuthorizationsListEvent, { authorizations: authorizations }, chain);
    }
}
