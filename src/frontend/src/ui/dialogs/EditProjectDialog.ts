import { defineAsyncComponent } from "vue";

import { type Project } from "@common/data/entities/Project";
import { extendedDialog, type ExtendedDialogResult } from "@common/ui/dialogs/ExtendedDialog";

import { type FrontendComponent } from "@/component/FrontendComponent";

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
export async function editProjectDialog(comp: FrontendComponent, project: Project | undefined): ExtendedDialogResult<EditProjectDialogData> {
    return extendedDialog<EditProjectDialogData>(comp, defineAsyncComponent(() => import("@/ui/dialogs/EditProjectDialog.vue")),
        {
            header: project ? "Edit Project" : "New Project",
            modal: true,
            contentClass: "w-[20vw] min-w-[25rem]"
        },
        {
            title: project?.title || "",
            description: project?.description || ""
        },
        {
            hasAcceptButton: true,
            acceptLabel: project ? "Save" : "Create",
            acceptIcon: "material-icons-outlined mi-done",

            hasRejectButton: true,
            rejectLabel: "Cancel",
            rejectIcon: "material-icons-outlined mi-clear"
        }
    );
}
