import { Type } from "class-transformer";

import { EventComposer } from "../../core/messaging/composers/EventComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Event } from "../../core/messaging/Event";
import { Message } from "../../core/messaging/Message";
import {
    Connector,
    type ConnectorCategoryID,
    type ConnectorID,
    ConnectorLogos,
    type ConnectorMetadataProfile,
    ConnectorOptions,
} from "../../data/entities/connector/Connector";

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

/**
 * Emitted by a connector to let the server know about its existence.
 */
@Message.define("event/connector/announce")
export class ConnectorAnnounceEvent extends Event {
    public readonly connector_id: ConnectorID = "";

    public readonly display_name: string = "";
    public readonly description: string = "";
    public readonly category: ConnectorCategoryID = "";

    public readonly options: ConnectorOptions = ConnectorOptions.Default;

    // @ts-ignore
    @Type(() => ConnectorLogos)
    public readonly logos: ConnectorLogos = new ConnectorLogos();

    public readonly metadata_profile: ConnectorMetadataProfile = {};

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        connectorID: ConnectorID,
        name: string,
        description: string,
        category: ConnectorCategoryID,
        options: ConnectorOptions,
        logos: ConnectorLogos,
        metadataProfile: ConnectorMetadataProfile,
        chain: Message | null = null,
    ): EventComposer<ConnectorAnnounceEvent> {
        return messageBuilder.buildEvent(
            ConnectorAnnounceEvent,
            {
                connector_id: connectorID,
                display_name: name,
                description: description,
                category: category,
                options: options,
                logos: logos,
                metadata_profile: metadataProfile,
            },
            chain,
        );
    }
}
