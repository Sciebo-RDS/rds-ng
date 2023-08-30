import { Type } from "class-transformer";

import { Channel } from "../core/messaging/Channel";
import { Event } from "../core/messaging/Event";
import { MessageEmitter } from "../core/messaging/handlers/MessageEmitter";
import { Message } from "../core/messaging/Message";
import { UnitID } from "../utils/UnitID";

/**
 * Emitted whenever the ``Client`` established a connection to a server.
 */
@Message.define("event/network/client-connected")
export class ClientConnectedEvent extends Event {
    /**
     * Helper function to easily emit this message.
     */
    public static emit(messageEmitter: MessageEmitter, target: Channel, chain: Message | null = null): void {
        messageEmitter.emitEvent(ClientConnectedEvent, target, {}, chain);
    }
}

/**
 * Emitted whenever the ``Client`` cuts its connection from the server.
 */
@Message.define("event/network/client-disconnected")
export class ClientDisconnectedEvent extends Event {
    /**
     * Helper function to easily emit this message.
     */
    public static emit(messageEmitter: MessageEmitter, target: Channel, chain: Message | null = null): void {
        messageEmitter.emitEvent(ClientDisconnectedEvent, target, {}, chain);
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
     * Helper function to easily emit this message.
     */
    public static emit(messageEmitter: MessageEmitter, target: Channel, reason: string, chain: Message | null = null): void {
        messageEmitter.emitEvent(ClientConnectionErrorEvent, target, { reason: reason }, chain);
    }
}

/**
 * Emitted whenever the ``Server`` established a connection to a client.
 */
@Message.define("event/network/server-connected")
class ServerConnectedEvent extends Event {
    @Type(() => UnitID)
    public readonly comp_id: UnitID = new UnitID("", "");
    public readonly client_id: string = "";

    /**
     * Helper function to easily emit this message.
     */
    public static emit(messageEmitter: MessageEmitter, target: Channel, compID: UnitID, clientID: string, chain: Message | null = null): void {
        messageEmitter.emitEvent(ServerConnectedEvent, target, { comp_id: compID, client_id: clientID }, chain);
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
     * Helper function to easily emit this message.
     */
    public static emit(messageEmitter: MessageEmitter, target: Channel, compID: UnitID, clientID: string, chain: Message | null = null): void {
        messageEmitter.emitEvent(ServerDisconnectedEvent, target, { comp_id: compID, client_id: clientID }, chain);
    }
}
