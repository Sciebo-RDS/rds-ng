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
@Message.define("event/job/list")
export class JobsListEvent extends Event {
    // @ts-ignore
    @Type(() => ProjectJob)
    public readonly project_jobs: ProjectJob[] = [];

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, projectJobs: ProjectJob[], chain: Message | null = null): EventComposer<JobsListEvent> {
        return messageBuilder.buildEvent(JobsListEvent, { project_jobs: projectJobs }, chain);
    }
}
