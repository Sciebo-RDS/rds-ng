import { UpdateProjectFeaturesCommand } from "@common/api/project/ProjectFeaturesCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import type { MetadataObjects } from "@common/data/entities/metadata/Types";
import { DataManagementPlanFeature } from "@common/data/entities/project/features/DataManagementPlanFeature";
import { ProjectFeature, type ProjectFeatureID } from "@common/data/entities/project/features/ProjectFeature";
import { ProjectFeatures } from "@common/data/entities/project/features/ProjectFeatures";
import { ProjectMetadataFeature } from "@common/data/entities/project/features/ProjectMetadataFeature";
import { ResourcesMetadataFeature } from "@common/data/entities/project/features/ResourcesMetadataFeature";
import { Project } from "@common/data/entities/project/Project";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { StatusNotifier } from "@common/ui/actions/notifiers/StatusNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to update the features of a project.
 */
export class UpdateProjectFeaturesAction extends FrontendCommandAction<UpdateProjectFeaturesCommand, CommandComposer<UpdateProjectFeaturesCommand>> {
    public prepare(
        project: Project,
        updatedFeatures: ProjectFeature[],
        sharedPropertyObjects: MetadataObjects | undefined = undefined
    ): CommandComposer<UpdateProjectFeaturesCommand> {
        this.prepareNotifiers(project.title);

        this._composer = UpdateProjectFeaturesCommand.build(
            this.messageBuilder,
            project.project_id,
            updatedFeatures.map((feature) => feature.featureID),
            new ProjectFeatures(
                this.getFeatureFromArray<ProjectMetadataFeature>(updatedFeatures, ProjectMetadataFeature.FeatureID),
                this.getFeatureFromArray<ResourcesMetadataFeature>(updatedFeatures, ResourcesMetadataFeature.FeatureID),
                this.getFeatureFromArray<DataManagementPlanFeature>(updatedFeatures, DataManagementPlanFeature.FeatureID)
            ),
            sharedPropertyObjects
        );
        return this._composer;
    }

    protected addDefaultNotifiers(title: string): void {
        this.addNotifier(
            ActionState.Executing,
            new StatusNotifier(OverlayNotificationType.Info, `Saving project '${title}'...`, "material-icons-outlined mi-save")
        );
        this.addNotifier(
            ActionState.Done,
            new StatusNotifier(OverlayNotificationType.Success, `Project '${title}' has been saved.`, "material-icons-outlined mi-save")
        );
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(
                OverlayNotificationType.Error,
                "Error updating project",
                `An error occurred while updating the features of project '${title}': ${ActionNotifier.MessagePlaceholder}.`,
                true
            )
        );
    }

    private getFeatureFromArray<FeatureType>(features: ProjectFeature[], featureID: ProjectFeatureID): FeatureType | undefined {
        for (const feature of features) {
            if (feature.featureID == featureID) {
                return feature as FeatureType;
            }
        }
        return undefined;
    }
}
