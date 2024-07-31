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
    newProject: boolean;
    title: string;
    description: string;
    datapath: string;
    options: ProjectOptions;
}

/**
 * Shows the edit dialog for a project.
 *
 * @param comp - The global component.
 * @param project - The project to edit.
 */
export async function editProjectDialog(comp: FrontendComponent, project?: Project): ExtendedDialogResult<EditProjectDialogData> {
    const newProject = !project;

    return extendedDialog<EditProjectDialogData>(
        comp,
        defineAsyncComponent(() => import("@/ui/dialogs/project/edit/EditProjectDialog.vue")),
        {
            header: project ? "Project settings" : "New project",
            modal: true,
            contentClass: newProject ? "w-[46rem] h-[44rem] pb-0" : "w-[46rem] h-[39rem] pb-0"
        },
        {
            newProject: newProject,
            title: project?.title || "",
            description: project?.description || "",
            datapath: project?.resources_path || "",
            options: deepClone<ProjectOptions>(project?.options, new ProjectOptions())
        },
        {
            hideFooter: newProject,

            hasAcceptButton: true,
            acceptLabel: project ? "Save" : "Create",
            acceptIcon: "material-icons-outlined mi-done",

            hasRejectButton: true,
            rejectLabel: "Cancel",
            rejectIcon: "material-icons-outlined mi-clear",

            showDataPathSelector: !project
        }
    );
}
