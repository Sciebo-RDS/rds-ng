import { UnitID } from "../../../utils/UnitID";
import { Message } from "../Message";
import { MessageMetaInformation } from "../meta/MessageMetaInformation";

/**
 * Enum telling the direction (INcoming or OUTgoing) of a message.
 */
export enum NetworkRouterDirection {
    In,
    Out
}

/**
 * Network routing rules and logic.
 *
 * When a message enters the network engine in order to be sent to remote targets, it is first checked for its
 * validity. Afterwards, the router decides through which channels (local, client) it needs to be sent.
 */
export class NetworkRouter {
    private readonly _compID: UnitID;

    /**
     * @param compID - The component id (required to decide whether we match a given direct target).
     */
    public constructor(compID: UnitID) {
        this._compID = compID;
    }

    /**
     * Verifies whether a message may enter the network engine.
     *
     * @param direction - The direction (*IN* or *OUT*) of the message.
     * @param msg - The message that wants to enter the network engine.
     *
     * @throws Error - In case the message is not valid to enter the network engine.
     */
    public verifyMessage(direction: NetworkRouterDirection, msg: Message): void {
        if (msg.target.isLocal) {
            this.verifyLocalMessage(direction, msg);
        } else if (msg.target.isDirect) {
            this.verifyDirectMessage(direction, msg);
        }
    }

    /**
     * Checks if the message should be routed locally (dispatched via the message bus).
     *
     * @param direction - The direction (*IN* or *OUT*) of the message.
     * @param msg - The actual message.
     * @param msgMeta - The message meta information.
     *
     * @returns Whether local routing should happen.
     */
    public checkLocalRouting(direction: NetworkRouterDirection, msg: Message, msgMeta: MessageMetaInformation): boolean {
        if (direction == NetworkRouterDirection.Out) {
            return false;  // Outgoing messages are never routed back locally
        } else if (direction == NetworkRouterDirection.In) {
            if (msg.target.isDirect && msg.target.targetID) {
                return msg.target.targetID.equals(this._compID);
            }
        }

        return false;
    }

    /**
     * Checks if the message should be routed through the client.
     *
     * @param direction - The direction (*IN* or *OUT*) of the message.
     * @param msg - The actual message.
     * @param msgMeta - The message meta information.
     *
     * @returns Whether client routing should happen.
     */
    public checkClientRouting(direction: NetworkRouterDirection, msg: Message, msgMeta: MessageMetaInformation): boolean {
        // Only send outgoing messages through the client
        return direction == NetworkRouterDirection.Out;
    }

    private verifyLocalMessage(direction: NetworkRouterDirection, msg: Message): void {
        // Local messages should never land here
        throw new Error("A local message was directed to the network engine");
    }

    private verifyDirectMessage(direction: NetworkRouterDirection, msg: Message): void {
        // An incoming direct message must be targeted to a component
        if (!msg.target.targetID) {
            throw new Error("Direct message without a target received");
        }

        // Outgoing direct messages may not be directed to this component
        if (direction == NetworkRouterDirection.Out) {
            if (msg.target.targetID.equals(this._compID)) {
                throw new Error("Direct message to this component sent through the network engine");
            }
        }
    }
}
