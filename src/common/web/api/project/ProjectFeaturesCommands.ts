import { Type } from "class-transformer";

import { Command } from "../../core/messaging/Command";
import { CommandReply } from "../../core/messaging/CommandReply";
import { CommandComposer } from "../../core/messaging/composers/CommandComposer";
import { CommandReplyComposer } from "../../core/messaging/composers/CommandReplyComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Message } from "../../core/messaging/Message";
import { type MetadataObjects } from "../../data/entities/metadata/Types";
import { type ProjectFeatureID } from "../../data/entities/project/features/ProjectFeature";
import { ProjectFeatures } from "../../data/entities/project/features/ProjectFeatures";
import { type ProjectID } from "../../data/entities/project/Project";
import { SharedPropertyObject } from "../../ui/components/propertyeditor/PropertyObjectStore";

/**
 * Command to update the features (data) of a project.
 *
 * @param project_id - The ID of the project to update.
 * @param updated_features - List of all features (using their ID) to update.
 * @param features - The new features data.
 * @param shared_objects - Optionally updated project-wide shared objects.
 */
@Message.define("command/project/features/update")
export class UpdateProjectFeaturesCommand extends Command {
    public readonly project_id: ProjectID = 0;

    // @ts-ignore
    @Type(() => String)
    public readonly updated_features: ProjectFeatureID[] = [];
    // @ts-ignore
    @Type(() => ProjectFeatures)
    public readonly features: ProjectFeatures = new ProjectFeatures();

    // @ts-ignore
    @Type(() => SharedPropertyObject)
    public readonly shared_objects: MetadataObjects | undefined = undefined;

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        project_id: ProjectID,
        updatedFeatures: ProjectFeatureID[],
        features: ProjectFeatures,
        sharedPropertyObjects: MetadataObjects | undefined = undefined,
        chain: Message | null = null
    ): CommandComposer<UpdateProjectFeaturesCommand> {
        return messageBuilder.buildCommand(
            UpdateProjectFeaturesCommand,
            {
                project_id: project_id,
                updated_features: updatedFeatures,
                features: features,
                shared_objects: sharedPropertyObjects
            },
            chain
        );
    }
}

/**
 * Reply to ``UpdateProjectFeaturesCommand``.
 *
 * @param project_id - The ID of the updated project.
 * @param updated_features - List of all updated features (using their ID).
 */
@Message.define("command/project/features/update/reply")
export class UpdateProjectFeaturesReply extends CommandReply {
    public readonly project_id: ProjectID = 0;

    // @ts-ignore
    @Type(() => String)
    public readonly updated_features: ProjectFeatureID[] = [];

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: UpdateProjectFeaturesReply,
        project_id: ProjectID,
        updated_features: ProjectFeatureID[],
        success: boolean = true,
        message: string = ""
    ): CommandReplyComposer<UpdateProjectFeaturesReply> {
        return messageBuilder.buildCommandReply(UpdateProjectFeaturesReply, cmd, success, message, {
            project_id: project_id,
            updated_features: updated_features
        });
    }
}
