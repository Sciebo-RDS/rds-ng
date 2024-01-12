import { Type } from "class-transformer";

import { EventComposer } from "../../core/messaging/composers/EventComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Event } from "../../core/messaging/Event";
import { Message } from "../../core/messaging/Message";
import { UserConfiguration } from "../../data/entities/user/UserConfiguration";

/**
 * Emitted whenever the user configuration has changed.
 *
 * @param configuration - The user configuration.
 */
@Message.define("event/user/configuration")
export class UserConfigurationEvent extends Event {
    // @ts-ignore
    @Type(() => UserConfiguration)
    public readonly configuration: UserConfiguration = new UserConfiguration();

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, configuration: UserConfiguration, chain: Message | null = null): EventComposer<UserConfigurationEvent> {
        return messageBuilder.buildEvent(UserConfigurationEvent, { configuration: configuration }, chain);
    }
}
