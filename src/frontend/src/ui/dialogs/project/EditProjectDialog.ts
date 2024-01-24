import { defineAsyncComponent } from "vue";

import { Project } from "@common/data/entities/project/Project";
import { ProjectOptions } from "@common/data/entities/project/ProjectOptions";
import { extendedDialog, type ExtendedDialogResult } from "@common/ui/dialogs/ExtendedDialog";
import { deepClone } from "@common/utils/ObjectUtils";

import { FrontendComponent } from "@/component/FrontendComponent";

/**
 * The data used by the ``editProjectDialog`` function.
 */
export interface EditProjectDialogData {
    title: string;
    description: string;
    options: ProjectOptions,
}

/**
 * Shows the edit dialog for a project.
 *
 * @param comp - The global component.
 * @param project - The project to edit.
 */
export async function editProjectDialog(
    comp: FrontendComponent,
    project: Project | undefined
): ExtendedDialogResult<EditProjectDialogData> {
    return extendedDialog<EditProjectDialogData>(
        comp,
        defineAsyncComponent(
            () => import("@/ui/dialogs/project/EditProjectDialog.vue")
        ),
        {
            header: project ? "Project settings" : "New project",
            modal: true,
            contentClass: "w-[20vw] w-full min-w-[40rem] !pt-4"
        },
        {
            title: project?.title || "",
            description: project?.description || "",
            options: deepClone<ProjectOptions>(project?.options, new ProjectOptions())
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
