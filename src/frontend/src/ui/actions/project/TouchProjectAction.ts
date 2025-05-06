import { ProjectTouchEvent } from "@common/api/project/ProjectEvents.ts";
import { EventComposer } from "@common/core/messaging/composers/EventComposer.ts";
import { type ProjectID } from "@common/data/entities/project/Project";

import { FrontendEventAction } from "@/ui/actions/FrontendEventAction.ts";

/**
 * Action to touch a project.
 */
export class TouchProjectAction extends FrontendEventAction<ProjectTouchEvent, EventComposer<ProjectTouchEvent>> {
    public prepare(projectID: ProjectID): EventComposer<ProjectTouchEvent> {
        super.prepareNotifiers(projectID);

        this._composer = ProjectTouchEvent.build(this.messageBuilder, projectID);
        return this._composer;
    }
}
