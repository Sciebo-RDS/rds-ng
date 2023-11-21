import { type Project } from "@common/data/entities/Project";

import { type FrontendComponent } from "@/component/FrontendComponent";
import { editDialog, type EditDialogResult } from "@common/ui/dialogs/EditDialog";
import { defineAsyncComponent } from "vue";

/**
 * The data used by the ``EditProjectDialog``.
 */
export interface EditProjectDialogData {
    title: string;
    description: string;
}

/**
 * Shows the edit dialog for a project.
 *
 * @param comp - The global component.
 * @param project - The project to edit.
 */
export async function editProjectDialog(comp: FrontendComponent, project: Project | undefined): EditDialogResult<EditProjectDialogData> {
    return editDialog<EditProjectDialogData>(comp, defineAsyncComponent(() => import("@/ui/dialogs/EditProjectDialog.vue")),
        {
            header: project ? "Edit Project" : "New Project",
            modal: true
        },
        {
            title: project?.title || "",
            description: project?.description || ""
        },
        {
            acceptLabel: project ? "Save" : "Create"
        }
    );
}
