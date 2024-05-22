import { InitiateProjectJobCommand } from "@common/api/project/ProjectJobCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { Connector } from "@common/data/entities/connector/Connector";
import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { Project } from "@common/data/entities/project/Project";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { findConnectorCategory } from "@/data/entities/connector/ConnectorUtils";
import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to initiate a project job.
 */
export class InitiateProjectJobAction extends FrontendCommandAction<InitiateProjectJobCommand, CommandComposer<InitiateProjectJobCommand>> {
    public prepare(project: Project, connector: Connector, connectorInstance: ConnectorInstance): CommandComposer<InitiateProjectJobCommand> {
        super.prepareNotifiers(project, connector, connectorInstance);

        this._composer = InitiateProjectJobCommand.build(this.messageBuilder, project.project_id, connectorInstance.instance_id).timeout(this._regularTimeout);
        return this._composer;
    }

    protected addDefaultNotifiers(project: Project, connector: Connector, connectorInstance: ConnectorInstance): void {
        const category = findConnectorCategory(connector);

        this.addNotifier(
            ActionState.Executing,
            new OverlayNotifier(
                OverlayNotificationType.Info,
                "Initiating job",
                `${category?.verbNoun} of project '${project.title}' through connection ${connectorInstance.name} is being started...`,
            ),
        );
        this.addNotifier(
            ActionState.Done,
            new OverlayNotifier(
                OverlayNotificationType.Success,
                "Initiating job",
                `${category?.verbNoun} of project '${project.title}' through connection ${connectorInstance.name} has been started`,
            ),
        );
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(
                OverlayNotificationType.Error,
                "Error initiating job",
                `An error occurred while starting the ${category?.verbNoun.toLowerCase()} of project '${project.title}': ${ActionNotifier.MessagePlaceholder}.`,
                true,
            ),
        );
    }
}
