import { Type } from "class-transformer";

import { EventComposer } from "../core/messaging/composers/EventComposer";
import { MessageBuilder } from "../core/messaging/composers/MessageBuilder";
import { Event } from "../core/messaging/Event";
import { Message } from "../core/messaging/Message";
import { UnitID } from "../utils/UnitID";

/**
 * Emitted whenever the ``Client`` established a connection to a server.
 */
@Message.define("event/network/client-connected")
export class ClientConnectedEvent extends Event {
    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, chain: Message | null = null): EventComposer<ClientConnectedEvent> {
        return messageBuilder.buildEvent(ClientConnectedEvent, {}, chain);
    }
}

/**
 * Emitted whenever the ``Client`` cuts its connection from the server.
 */
@Message.define("event/network/client-disconnected")
export class ClientDisconnectedEvent extends Event {
    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, chain: Message | null = null): EventComposer<ClientDisconnectedEvent> {
        return messageBuilder.buildEvent(ClientDisconnectedEvent, {}, chain);
    }
}

/**
 * Emitted whenever the ``Client`` is unable to establish a connection.
 *
 * @param reason - The connection error reason.
 */
@Message.define("event/network/client-connection-error")
export class ClientConnectionErrorEvent extends Event {
    public readonly reason: string = "";

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, reason: string, chain: Message | null = null): EventComposer<ClientConnectionErrorEvent> {
        return messageBuilder.buildEvent(ClientConnectionErrorEvent, { reason: reason }, chain);
    }
}

/**
 * Emitted whenever the ``Server`` established a connection to a client.
 */
@Message.define("event/network/server-connected")
class ServerConnectedEvent extends Event {
    // @ts-ignore
    @Type(() => UnitID)
    public readonly comp_id: UnitID = new UnitID("", "");
    public readonly client_id: string = "";

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, compID: UnitID, clientID: string, chain: Message | null = null):
        EventComposer<ServerConnectedEvent> {
        return messageBuilder.buildEvent(ServerConnectedEvent, { comp_id: compID, client_id: clientID }, chain);
    }
}

/**
 * Emitted whenever the ``Server`` cuts a connection from a client.
 */
@Message.define("event/network/server-disconnected")
export class ServerDisconnectedEvent extends Event {
    public readonly comp_id: UnitID = new UnitID("", "");
    public readonly client_id: string = "";

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, compID: UnitID, clientID: string, chain: Message | null = null):
        EventComposer<ServerDisconnectedEvent> {
        return messageBuilder.buildEvent(ServerDisconnectedEvent, { comp_id: compID, client_id: clientID }, chain);
    }
}
