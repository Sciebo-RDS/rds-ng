import { type Project } from "@common/data/entities/Project";
import { confirmDialog, type ConfirmDialogResult } from "@common/ui/dialogs/ConfirmDialog";

import { type FrontendComponent } from "@/component/FrontendComponent";

export async function editProjectDialog(comp: FrontendComponent, project: Project): ConfirmDialogResult {
    return confirmDialog(comp, {
            group: "templating",
            header: "Edit project",

            message: "Please confirm to proceed moving forward.",
            icon: "pi pi-exclamation-circle",
            acceptIcon: "pi pi-check",
            rejectIcon: "pi pi-times",
            rejectClass: "p-button-sm",
            acceptClass: "p-button-outlined p-button-sm"
        }
    );
}
