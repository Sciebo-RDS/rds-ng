import { UpdateProjectFeaturesCommand } from "@common/api/project/ProjectFeaturesCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { DataManagementPlanFeature } from "@common/data/entities/project/features/DataManagementPlanFeature";
import { ProjectMetadataFeature } from "@common/data/entities/project/features/ProjectMetadataFeature";
import { ProjectFeature, type ProjectFeatureID } from "@common/data/entities/project/features/ProjectFeature";
import { ProjectFeatures } from "@common/data/entities/project/features/ProjectFeatures";
import { ResourcesMetadataFeature } from "@common/data/entities/project/features/ResourcesMetadataFeature";
import { Project } from "@common/data/entities/project/Project";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to update the features of a project.
 */
export class UpdateProjectFeaturesAction extends FrontendCommandAction<UpdateProjectFeaturesCommand, CommandComposer<UpdateProjectFeaturesCommand>> {
    public prepare(project: Project, updatedFeatures: ProjectFeature[]): CommandComposer<UpdateProjectFeaturesCommand> {
        this.prepareNotifiers(project.title);

        this._composer = UpdateProjectFeaturesCommand.build(
            this.messageBuilder,
            project.project_id,
            updatedFeatures.map((feature) => feature.featureID),
            new ProjectFeatures(
                this.getFeatureFromArray<ProjectMetadataFeature>(updatedFeatures, ProjectMetadataFeature.FeatureID),
                this.getFeatureFromArray<ResourcesMetadataFeature>(updatedFeatures, ResourcesMetadataFeature.FeatureID),
                this.getFeatureFromArray<DataManagementPlanFeature>(updatedFeatures, DataManagementPlanFeature.FeatureID)
            )
        );
        return this._composer;
    }

    protected addDefaultNotifiers(title: string): void {
        this.addNotifier(
            ActionState.Executing,
            new OverlayNotifier(OverlayNotificationType.Info, "Updating project", `Project '${title}' is being updated...`),
            true
        );
        this.addNotifier(
            ActionState.Done,
            new OverlayNotifier(OverlayNotificationType.Success, "Updating project", `Project '${title}' has been updated.`),
            true
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
