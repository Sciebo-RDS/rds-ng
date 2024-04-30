import { Type } from "class-transformer";

import { EventComposer } from "../../core/messaging/composers/EventComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Event } from "../../core/messaging/Event";
import { Message } from "../../core/messaging/Message";
import { type ConnectorInstanceID } from "../../data/entities/connector/ConnectorInstance";
import { type ProjectID } from "../../data/entities/project/Project";
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

/**
 * Emitted to inform about the progression of a job.
 *
 * @param project_id - The project ID.
 * @param connector_instance - The connector instance ID.
 * @param progress - The total progress (0.0 - 1.0).
 * @param message - The current activity message.
 */
@Message.define("event/project-job/progress")
export class ProjectJobProgressEvent extends Event {
    public readonly project_id: ProjectID = 0;
    public readonly connector_instance: ConnectorInstanceID = "";

    public readonly progress: number = 0.0;
    public readonly message: string = "";

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        projectID: ProjectID,
        connectorInstance: ConnectorInstanceID,
        progress: number,
        message: string,
        chain: Message | null = null,
    ): EventComposer<ProjectJobProgressEvent> {
        return messageBuilder.buildEvent(
            ProjectJobProgressEvent,
            { project_id: projectID, connector_instance: connectorInstance, progress: progress, message: message },
            chain,
        );
    }
}
