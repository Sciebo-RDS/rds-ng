import { Type } from "class-transformer";

import { EventComposer } from "../../core/messaging/composers/EventComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Event } from "../../core/messaging/Event";
import { Message } from "../../core/messaging/Message";
import { UserSettings } from "../../data/entities/user/UserSettings";

/**
 * Event sent when the user settings have changed on the server side.
 *
 * @param settings - The new settings.
 */
@Message.define("event/user/settings/changed")
export class UserSettingsChangedEvent extends Event {
    // @ts-ignore
    @Type(() => UserSettings)
    public readonly settings: UserSettings = new UserSettings();

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, settings: UserSettings, chain: Message | null = null): EventComposer<UserSettingsChangedEvent> {
        return messageBuilder.buildEvent(UserSettingsChangedEvent, { settings: settings }, chain);
    }
}
