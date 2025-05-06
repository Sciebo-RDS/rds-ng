import { defineAsyncComponent } from "vue";

import { Project } from "@common/data/entities/project/Project";
import { extendedDialog, type ExtendedDialogResult } from "@common/ui/dialogs/ExtendedDialog";

import { FrontendComponent } from "@/component/FrontendComponent";

/**
 * The data used by the ``uploadProjectDialog`` function.
 */
export interface UploadProjectDialogData {
    project: Project;
}

/**
 * Shows the upload dialog for a project.
 *
 * @param comp - The global component.
 * @param project - The project to upload.
 */
export async function uploadProjectDialog(comp: FrontendComponent, project: Project): ExtendedDialogResult<UploadProjectDialogData> {
    return extendedDialog<UploadProjectDialogData>(
        comp,
        defineAsyncComponent(() => import("@/ui/dialogs/project/upload/UploadProjectDialog.vue")),
        {
            header: "Upload project",
            modal: true,
            contentClass: "w-[30vw] min-w-[48rem] h-[50rem]"
        },
        {
            project: project
        },
        {
            hasRejectButton: true,
            rejectLabel: "Close"
        }
    );
}
