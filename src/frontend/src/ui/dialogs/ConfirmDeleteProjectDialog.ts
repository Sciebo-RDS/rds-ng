import { type Project } from "@common/data/entities/project/Project";
import { confirmDialog, type ConfirmDialogResult } from "@common/ui/dialogs/ConfirmDialog";

import { type FrontendComponent } from "@/component/FrontendComponent";

/**
 * Shows a confirmation dialog for project deletion.
 *
 * @param comp - The global component.
 * @param project - The project to delete.
 */
export async function confirmDeleteProjectDialog(comp: FrontendComponent, project: Project): ConfirmDialogResult {
    return confirmDialog(comp, {
            header: "Delete project",
            message: `Do you really want to delete project '${project.title}' (ID: ${project.project_id})? This is a permanent operation and cannot be undone!`,
            acceptClass: "p-button-danger",
            icon: "material-icons-outlined mi-warning-amber",
            acceptIcon: "material-icons-outlined mi-delete-forever"
        }
    );
}
