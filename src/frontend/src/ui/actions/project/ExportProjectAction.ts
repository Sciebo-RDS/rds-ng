import { ExportProjectCommand } from "@common/api/project/ProjectExportersCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { type ProjectFeatureID } from "@common/data/entities/project/features/ProjectFeature";
import { Project } from "@common/data/entities/project/Project";
import { ProjectExporterDescriptor } from "@common/data/exporters/ProjectExporterDescriptor";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to export a project.
 */
export class ExportProjectAction extends FrontendCommandAction<ExportProjectCommand, CommandComposer<ExportProjectCommand>> {
    public prepare(project: Project, exporter: ProjectExporterDescriptor, scope: ProjectFeatureID): CommandComposer<ExportProjectCommand> {
        super.prepareNotifiers(project, exporter);

        this._composer = ExportProjectCommand.build(this.messageBuilder, project.project_id, exporter.exporter_id, scope);
        return this._composer;
    }

    protected addDefaultNotifiers(project: Project, exporter: ProjectExporterDescriptor): void {
        this.addNotifier(
            ActionState.Executing,
            new OverlayNotifier(
                OverlayNotificationType.Info,
                "Initiating export",
                `Export of project '${project.title}' to ${exporter.name} is being started...`
            ),
            true
        );
        this.addNotifier(
            ActionState.Done,
            new OverlayNotifier(
                OverlayNotificationType.Success,
                "Export finished",
                `Export of project '${project.title}' to ${exporter.name} has been finished`
            )
        );
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(
                OverlayNotificationType.Error,
                "Error exporting project",
                `An error occurred while exporting project '${project.title}': ${ActionNotifier.MessagePlaceholder}.`,
                true
            )
        );
    }
}
