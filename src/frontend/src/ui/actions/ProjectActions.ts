import { DeleteProjectAction } from "@/ui/actions/DeleteProjectAction";
import { Project, type ProjectID } from "@common/data/entities/Project";
import { optCall } from "@common/utils/Functional";

import { FrontendComponent } from "@/component/FrontendComponent";
import { CreateProjectAction } from "@/ui/actions/CreateProjectAction";
import { UpdateProjectAction } from "@/ui/actions/UpdateProjectAction";

/**
 * A Composable to encapsulate all project actions.
 *
 * @param comp - The global frontend component.
 */
export function projectActions(comp: FrontendComponent) {
    function createProject(cb: ((title: string, description: string) => void) | undefined = undefined) {
        const action = new CreateProjectAction(comp);
        action.showEditDialog().then((data) => {
            action.prepare(data.title, data.description);
            action.execute();

            optCall(cb, data.title, data.description);
        });
    }

    function editProject(project: Project, cb: ((projectID: ProjectID, title: string, description: string) => void) | undefined = undefined) {
        const action = new UpdateProjectAction(comp);
        action.showEditDialog(project).then((data) => {
            action.prepare(project.project_id, data.title, data.description);
            action.execute();

            optCall(cb, project.project_id, data.title, data.description);
        });
    }

    function deleteProject(project: Project, cb: ((projectID: ProjectID) => void) | undefined = undefined) {
        const action = new DeleteProjectAction(comp);
        action.showConfirmation(project).then(() => {
            action.prepare(project);
            action.execute();

            optCall(cb, project.project_id);
        });
    }

    return {
        createProject,
        editProject,
        deleteProject
    };
}
