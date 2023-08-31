import { Type } from "class-transformer";

import { EventComposer } from "../core/messaging/builders/EventComposer";
import { MessageBuilder } from "../core/messaging/builders/MessageBuilder";
import { Event } from "../core/messaging/Event";
import { Message } from "../core/messaging/Message";
import { UnitID } from "../utils/UnitID";
import { API_PROTOCOL_VERSION } from "./Version";

/**
 * Contains information about a connected component; this is automatically sent whenever a connection is established (bilaterally).
 *
 * @param comp_id - The component ID.
 * @param comp_name - The component name.
 * @param comp_version - The component version.
 * @param api_protocol - The API protocol version.
 */
@Message.define("event/component/information")
export class ComponentInformationEvent extends Event {
    // @ts-ignore
    @Type(() => UnitID)
    public readonly comp_id: UnitID = new UnitID("", "");

    public readonly comp_name: string = "";
    public readonly comp_version: string = "";

    public readonly api_protocol: number = API_PROTOCOL_VERSION;

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, compID: UnitID, compName: string, compVersion: string,
                        chain: Message | null = null): EventComposer<ComponentInformationEvent> {
        return messageBuilder.buildEvent(ComponentInformationEvent,
            {
                comp_id: compID,
                comp_name: compName,
                comp_version: compVersion
            }, chain);
    }
}
