import { Project } from "@common/data/entities/project/Project";

import { FrontendComponent } from "@/component/FrontendComponent";
import { CreateProjectAction } from "@/ui/actions/project/CreateProjectAction";
import { DeleteProjectAction } from "@/ui/actions/project/DeleteProjectAction";
import { PublishProjectAction } from "@/ui/actions/project/PublishProjectAction";
import { UpdateProjectAction } from "@/ui/actions/project/UpdateProjectAction";

/**
 * Tools for working with projects.
 */
export function useProjectTools(comp: FrontendComponent) {
    function newProject(): Promise<void> {
        const action = new CreateProjectAction(comp);
        return action.showEditDialog().then((data) => {
            action.prepare(data.datapath, data.title, data.description, data.options);
            action.execute();
        });
    }

    function editProject(project: Project): Promise<void> {
        const action = new UpdateProjectAction(comp);
        return action.showEditDialog(project).then((data) => {
            action.prepare(project.project_id, data.title, data.description, data.options);
            action.execute();
        });
    }

    function publishProject(project: Project): Promise<void> {
        const action = new PublishProjectAction(comp);
        return action.showPublishDialog(project).then((data) => {
            // TODO
        });
    }

    function deleteProject(project: Project): void {
        const action = new DeleteProjectAction(comp);
        action.showConfirmation(project).then(() => {
            action.prepare(project);
            action.execute();
        });
    }

    return {
        newProject,
        editProject,
        publishProject,
        deleteProject
    };
}
