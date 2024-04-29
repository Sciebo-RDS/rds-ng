import { Type } from "class-transformer";

import { EventComposer } from "../../core/messaging/composers/EventComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Event } from "../../core/messaging/Event";
import { Message } from "../../core/messaging/Message";
import { ProjectJob } from "../../data/entities/project/ProjectJob";

/**
 * Emitted whenever the user's project jobs list has been updated.
 *
 * @param projects - The projects list.
 */
@Message.define("event/project-job/list")
export class ProjectJobsListEvent extends Event {
    // @ts-ignore
    @Type(() => ProjectJob)
    public readonly jobs: ProjectJob[] = [];

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, jobs: ProjectJob[], chain: Message | null = null): EventComposer<ProjectJobsListEvent> {
        return messageBuilder.buildEvent(ProjectJobsListEvent, { jobs: jobs }, chain);
    }
}
