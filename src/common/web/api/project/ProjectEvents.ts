import { Type } from "class-transformer";

import { EventComposer } from "../../core/messaging/composers/EventComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Event } from "../../core/messaging/Event";
import { Message } from "../../core/messaging/Message";
import { ProjectLogbook } from "../../data/entities/project/logbook/ProjectLogbook";
import { Project, type ProjectID } from "../../data/entities/project/Project";

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

/**
 * Emitted whenever the project's logbook has been updated.
 *
 * @param project_id - The project ID.
 * @param logbook - The new project logbook.
 */
@Message.define("event/project/logbook")
export class ProjectLogbookEvent extends Event {
    public readonly project_id: ProjectID = 0;

    // @ts-ignore
    @Type(() => ProjectLogbook)
    public readonly logbook: ProjectLogbook = new ProjectLogbook();

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        projectID: ProjectID,
        logbook: ProjectLogbook,
        chain: Message | null = null,
    ): EventComposer<ProjectLogbookEvent> {
        return messageBuilder.buildEvent(ProjectLogbookEvent, { project_id: projectID, logbook: logbook }, chain);
    }
}
