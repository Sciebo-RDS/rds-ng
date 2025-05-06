import { MessageContext } from "../core/messaging/handlers/MessageContext";

/**
 * An execution context for messages dispatched by the message bus to a service.
 *
 * This class is an extension to the more general ``MessageContext`` specifically used by ``Service`` and its message handlers.
 */
export class ServiceContext extends MessageContext {
}
