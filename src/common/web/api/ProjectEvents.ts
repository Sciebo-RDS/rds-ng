import { Type } from "class-transformer";

import { EventComposer } from "../core/messaging/composers/EventComposer";
import { MessageBuilder } from "../core/messaging/composers/MessageBuilder";
import { Event } from "../core/messaging/Event";
import { Message } from "../core/messaging/Message";
import { Project } from "../data/entities/Project";

/**
 * Emitted whenever the user's projects list has been updated.
 *
 * @param projects - The projects list.
 */
@Message.define("event/project/list")
export class ProjectsListEvent extends Event {
    // @ts-ignore
    @Type(() => Project)
    public readonly projects: Project[] = [];

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, projects: Project[], chain: Message | null = null): EventComposer<ProjectsListEvent> {
        return messageBuilder.buildEvent(ProjectsListEvent, { projects: projects }, chain);
    }
}
