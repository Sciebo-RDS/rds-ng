import { Event } from "../core/messaging/Event";
import { Message } from "../core/messaging/Message";

/**
 * Emitted whenever the ``Client`` established a connection to a server.
 */
@Message.define("event/network/client-connected")
export class ClientConnectedEvent extends Event {
}

/**
 * Emitted whenever the ``Client`` cuts its connection from the server.
 */
@Message.define("event/network/client-disconnected")
export class ClientDisconnectedEvent extends Event {
}

/**
 * Emitted whenever the ``Client`` is unable to establish a connection.
 *
 * @param reason - The connection error reason.
 */
@Message.define("event/network/client-connection-error")
export class ClientConnectionErrorEvent extends Event {
    public readonly reason: string = "";
}

/**
 * Emitted whenever the ``Server`` established a connection to a client.
 */
@Message.define("event/network/server-connected")
class ServerConnectedEvent extends Event {
    public readonly client_id: string = "";
}

/**
 * Emitted whenever the ``Server`` cuts a connection from a client.
 */
@Message.define("event/network/server-disconnected")
export class ServerDisconnectedEvent extends Event {
    public readonly client_id: string = "";
}
