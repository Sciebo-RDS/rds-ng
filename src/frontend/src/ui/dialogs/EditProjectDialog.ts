import { defineAsyncComponent } from "vue";

import { type ProjectFeatureID } from "@common/data/entities/EntityTypes";
import { type Project } from "@common/data/entities/Project";
import { extendedDialog, type ExtendedDialogResult } from "@common/ui/dialogs/ExtendedDialog";

import { type FrontendComponent } from "@/component/FrontendComponent";

/**
 * The data used by the ``EditProjectDialog``.
 */
export interface EditProjectDialogData {
    title: string;
    description: string;
    selectedFeatures: ProjectFeatureID[];
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
            header: project ? "Project settings" : "New project",
            modal: true,
            contentClass: "w-[20vw] min-w-[25rem]"
        },
        {
            title: project?.title || "",
            description: project?.description || "",
            selectedFeatures: project?.features_selection || []
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
