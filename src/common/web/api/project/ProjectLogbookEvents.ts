import { Type } from "class-transformer";

import { EventComposer } from "../../core/messaging/composers/EventComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Event } from "../../core/messaging/Event";
import { Message } from "../../core/messaging/Message";
import { ProjectLogbook } from "../../data/entities/project/logbook/ProjectLogbook";
import { type ProjectID } from "../../data/entities/project/Project";

/**
 * Sent whenever the logbook of a project has changed.
 *
 * @param project_id - The ID of the updated project.
 * @param logbook - The new logbook contents.
 */
@Message.define("event/project/logbook/update")
export class ProjectLogbookUpdateEvent extends Event {
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
    ): EventComposer<ProjectLogbookUpdateEvent> {
        return messageBuilder.buildEvent(ProjectLogbookUpdateEvent, { project_id: projectID, logbook: logbook }, chain);
    }
}
