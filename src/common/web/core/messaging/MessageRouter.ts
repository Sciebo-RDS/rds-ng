import { UnitID } from "../../utils/UnitID";
import { Message } from "./Message";
import { MessageEntrypoint, MessageMetaInformation } from "./meta/MessageMetaInformation";

/**
 * Message routing rules and logic.
 *
 * When a message enters the message bus, it is first checked for its validity.
 * Afterwards, the router decides through which channels (local, remote) it needs to be sent.
 */
export class MessageRouter {
    private readonly _compID: UnitID;

    /**
     * @param compID - The component id (required to decide whether we match a given direct target).
     */
    public constructor(compID: UnitID) {
        this._compID = compID;
    }

    /**
     * Verifies whether a message may enter the message bus.
     *
     * @param msg - The message that wants to enter the network engine.
     * @param msgMeta - The message meta information.
     *
     * @throws Error - In case the message is not valid to enter the message bus.
     */
    public verifyMessage(msg: Message, msgMeta: MessageMetaInformation): void {
        if (msg.target.isLocal) {
            this.verifyLocalMessage(msg, msgMeta);
        } else if (msg.target.isDirect) {
            this.verifyDirectMessage(msg, msgMeta);
        }
    }

    /**
     * Checks if the message should be routed locally.
     *
     * @param msg - The message.
     * @param msgMeta - The message meta information.
     */
    public checkLocalRouting(msg: Message, msgMeta: MessageMetaInformation): boolean {
        if (msg.target.isLocal) {
            return true;
        } else if (msg.target.isDirect && msg.target.targetID) {
            // A direct message that has made it to the message bus either stems from this component or is targeted to it
            // If it is targeted to this component, it needs to be dispatched locally
            return msg.target.targetID.equals(this._compID);
        }

        return false;
    }

    /**
     * Checks if the message should be routed remotely.
     *
     * @param msg - The message.
     * @param msgMeta - The message meta information.
     */
    public checkRemoteRouting(msg: Message, msgMeta: MessageMetaInformation): boolean {
        return !msg.target.isLocal && msgMeta.entrypoint == MessageEntrypoint.Local;
    }

    private verifyLocalMessage(msg: Message, msgMeta: MessageMetaInformation): void {
        if (msgMeta.entrypoint != MessageEntrypoint.Local) {
            throw new Error("Local message entering from a non-local location received");
        }
    }

    private verifyDirectMessage(msg: Message, msgMeta: MessageMetaInformation): void {
        if (!msg.target.targetID) {
            throw new Error("Direct message without a target received");
        }

        if (msgMeta.entrypoint == MessageEntrypoint.Local && msg.target.targetID.equals(this._compID)) {
            throw new Error("Message coming from this component directed to self");
        } else if (msgMeta.entrypoint != MessageEntrypoint.Local && !msg.target.targetID.equals(this._compID)) {
            throw new Error("Message coming from another component not directed to this component");
        }
    }
}
