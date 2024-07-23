<script setup lang="ts">
import { FrontendComponent } from "@/component/FrontendComponent";
import { confirmDialog } from "@common/ui/dialogs/ConfirmDialog";
import Button from "primevue/button";
import Menu from "primevue/menu";
import OverlayPanel from "primevue/overlaypanel";
import SplitButton from "primevue/splitbutton";
import { useDialog } from "primevue/usedialog";
import { computed, ref } from "vue";
import { SharedObject, dummyProjectObject } from "./ProjectObjectStore";
import PropertyDialog from "./PropertyDialog.vue";
import { calcBgColor, calcBorderColor, calcObjLabel } from "./utils/ObjectUtils";

// @ts-ignore
SplitButton.components.PVSMenu = Menu;
const comp = FrontendComponent.inject();
const dialog = useDialog();
const props = defineProps(["itemId", "parentId", "projectObjects", "sharedObjectStore", "projectProfiles", "mode"]);

const object = computed(() => {
    const obj = props.sharedObjectStore.get(props.itemId) || (dummyProjectObject(props.itemId) as SharedObject);
    if (obj["type"] === "dummy") props.projectObjects.removeRef(props.parentId, props.itemId);
    return obj;
});

const instanceLabel = computed(() => calcObjLabel(object.value, props.projectProfiles));
const linkedItemActions = computed(() => [
    {
        label: `${instanceLabel.value}`,
        hasSubmenu: false,
        items: [
            {
                label: "Edit",
                icon: "pi pi-pencil",
                command: () => {
                    handleClick();
                }
            },
            {
                label: `Unlink`,
                icon: "pi pi-minus",
                command: () => {
                    confirmDialog(comp, {
                        header: `Unlink "${instanceLabel.value}?"`,
                        message: "Are you sure you want to unlink this property? The object will not be deleted, you can relink at any time.",
                        acceptLabel: "Unlink",
                        acceptIcon: "pi pi-minus",
                        acceptClass: "p-button-danger",
                        rejectLabel: "Cancel",
                        rejectIcon: "pi pi-times",
                        rejectClass: "p-button-secondary"
                    }).then(() => {
                        console.log("Unlinking " + object.value.id);
                        props.projectObjects.removeRef(props.parentId, object.value.id);
                        props.sharedObjectStore.removeRef(props.parentId, object.value.id);
                    });
                }
            },
            {
                label: "Delete",
                icon: "pi pi-trash",
                command: () => {
                    confirmDialog(comp, {
                        header: `Delete "${instanceLabel.value}"?`,
                        message: "Are you sure you want to delete this object? It will not be recoverable.",
                        acceptLabel: "Delete",
                        acceptIcon: "pi pi-trash",
                        acceptClass: "p-button-danger",
                        rejectLabel: "Cancel",
                        rejectIcon: "pi pi-times",
                        rejectClass: "p-button-secondary"
                    }).then(() => {
                        console.log("Deleting " + object.value.id);
                        props.projectObjects.remove(object.value.id);
                        props.sharedObjectStore.remove(object.value.id);
                    });
                }
            }
        ]
    }
]);

const emit = defineEmits(["loadObject"]);
function handleClick() {
    if (props.mode == "dialog") {
        emit("loadObject", object.value["id"]);
    } else {
        dialog.open(PropertyDialog, {
            props: {
                header: "Edit Property",
                style: {
                    width: "50vw",
                    height: "80vh"
                },
                breakpoints: {
                    "960px": "75vw",
                    "640px": "90vw"
                },
                modal: true,
                dismissableMask: true
            },
            data: {
                id: object.value["id"],
                projectObjects: props.projectObjects,
                sharedObjectStore: props.sharedObjectStore,
                projectProfiles: props.projectProfiles
            }
        });
    }
}

const op = ref();
const toggle = (event: Event) => {
    op.value.toggle(event);
};
</script>

<template>
    <div :title="JSON.stringify(object, null, 4)" @contextmenu="(e: Event) => e.preventDefault()">
        <SplitButton
            ref="button"
            menuButtonIcon="pi pi-ellipsis-v"
            :model="linkedItemActions"
            menuitemicon="pi pi-link"
            class="min-h-full py-0 my-0 mb-2 space-y-0 w-full"
            @click="handleClick"
            @contextmenu="
                () => {
                    const button = $refs.button as typeof ref<SplitButton>;
                    //@ts-ignore
                    button.onDropdownButtonClick();
                }
            "
            :style="`--p-color: ${calcBgColor(object, props.projectProfiles)}; --p-border-color: ${calcBorderColor(object, props.projectProfiles)};`"
        >
            <span class="mx-2 truncate flex items-center space-x-2">
                <span class="text-sm text-gray-700">
                    {{ props.projectProfiles.getClassLabelById(object["type"]) }}
                </span>
                <span class="text-lg text-gray-800 truncate">
                    {{ instanceLabel }}
                </span>
            </span>
        </SplitButton>

        <OverlayPanel ref="op" class="border-red-400">
            <div class="m-2 gap-3 w-25rem">
                <div>
                    <span class="font-medium text-900 block mb-2">The linked object is missing.</span>
                </div>
                <div>Do you want to remove all links to the missing object?</div>
                <div class="min-w-full flex justify-end mt-5 space-x-2">
                    <Button text class="min-w-fit" size="small" @click="toggle"> cancel </Button>
                    <Button
                        class="min-w-fit"
                        size="small"
                        severity="danger"
                        icon="pi pi-trash"
                        @click="
                            () => {
                                props.sharedObjectStore.remove(props.itemId, props.itemId);
                                props.projectObjects.remove(props.itemId, props.itemId);
                            }
                        "
                    >
                        Remove
                    </Button>
                </div>
            </div>
        </OverlayPanel>
    </div>
</template>

<style scoped lang="scss">
.p-splitbutton {
    @apply h-8 text-gray-600 border border-[var(--p-border-color)];
}
:deep(.p-splitbutton-defaultbutton) {
    @apply bg-[var(--p-color)] bg-opacity-30 border-0 px-2 text-inherit;
}

:deep(.p-splitbutton-menubutton) {
    @apply bg-[var(--p-color)] bg-opacity-50 border-0 border-l border-[var(--p-border-color)] text-inherit;
}
</style>
