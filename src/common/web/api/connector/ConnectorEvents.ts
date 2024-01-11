import { Type } from "class-transformer";

import { EventComposer } from "../../core/messaging/composers/EventComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Event } from "../../core/messaging/Event";
import { Message } from "../../core/messaging/Message";
import { Connector } from "../../data/entities/Connector";

/**
 * Emitted whenever the list of available connectors has been updated.
 *
 * @param connectors - List of all connectors.
 */
@Message.define("event/connector/list")
export class ConnectorsListEvent extends Event {
    // @ts-ignore
    @Type(() => Connector)
    public readonly connectors: Connector[] = [];

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, connectors: Connector[], chain: Message | null = null): EventComposer<ConnectorsListEvent> {
        return messageBuilder.buildEvent(ConnectorsListEvent, { connectors: connectors }, chain);
    }
}
