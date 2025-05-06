import { Type } from "class-transformer";

import { EventComposer } from "../../core/messaging/composers/EventComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Event } from "../../core/messaging/Event";
import { Message } from "../../core/messaging/Message";
import { type ConnectorInstanceID } from "../../data/entities/connector/ConnectorInstance";
import { ProjectLogbook } from "../../data/entities/project/logbook/ProjectLogbook";
import { Project, type ProjectID } from "../../data/entities/project/Project";
import { ProjectExternalState, ProjectUploadState } from "../../data/entities/project/ProjectExternalState";
import { type UserID } from "../../data/entities/user/User";

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
 * Emitted whenever a project has been "touched" (i.e., selected/activated) by the user.
 *
 * @param project_id - The project ID.
 */
@Message.define("event/project/touch")
export class ProjectTouchEvent extends Event {
    public readonly project_id: ProjectID = 0;

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, projectID: ProjectID, chain: Message | null = null): EventComposer<ProjectTouchEvent> {
        return messageBuilder.buildEvent(ProjectTouchEvent, { project_id: projectID }, chain);
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
        chain: Message | null = null
    ): EventComposer<ProjectLogbookEvent> {
        return messageBuilder.buildEvent(ProjectLogbookEvent, { project_id: projectID, logbook: logbook }, chain);
    }
}

/**
 * Emitted whenever the external state of a project has been updated.
 *
 * @param project_id - The project ID.
 * @param user_id - The user ID.
 * @param connector_instance - The connector instance ID.
 * @param external_state - The new project's external state.
 */
@Message.define("event/project/external-state")
export class ProjectExternalStateEvent extends Event {
    public readonly project_id: ProjectID = 0;
    public readonly user_id: UserID = "";
    public readonly connector_instance: ConnectorInstanceID = "";

    // @ts-ignore
    @Type(() => ProjectExternalState)
    public readonly external_state: ProjectExternalState = new ProjectExternalState(ProjectUploadState.Unknown, "");

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        userID: UserID,
        projectID: ProjectID,
        connector_instance: ConnectorInstanceID,
        external_state: ProjectExternalState,
        chain: Message | null = null
    ): EventComposer<ProjectLogbookEvent> {
        return messageBuilder.buildEvent(
            ProjectLogbookEvent,
            { project_id: projectID, user_id: userID, connector_instance: connector_instance, external_state: external_state },
            chain
        );
    }
}
