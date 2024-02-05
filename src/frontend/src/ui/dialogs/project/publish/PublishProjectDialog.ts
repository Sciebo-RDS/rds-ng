import { defineAsyncComponent } from "vue";

import { Project } from "@common/data/entities/project/Project";
import { extendedDialog, type ExtendedDialogResult } from "@common/ui/dialogs/ExtendedDialog";

import { FrontendComponent } from "@/component/FrontendComponent";

/**
 * The data used by the ``publishProjectDialog`` function.
 */
export interface PublishProjectDialogData {
}

/**
 * Shows the publish dialog for a project.
 *
 * @param comp - The global component.
 * @param project - The project to publish.
 */
export async function publishProjectDialog(
    comp: FrontendComponent,
    project: Project
): ExtendedDialogResult<PublishProjectDialogData> {
    return extendedDialog<PublishProjectDialogData>(
        comp,
        defineAsyncComponent(
            () => import("@/ui/dialogs/project/publish/PublishProjectDialog.vue")
        ),
        {
            header: "Publish & Export project",
            modal: true,
            contentClass: "w-[20vw] min-w-[40rem] !pt-4"
        },
        {},
        {
            hasRejectButton: true,
            rejectLabel: "Close"
        }
    );
}
