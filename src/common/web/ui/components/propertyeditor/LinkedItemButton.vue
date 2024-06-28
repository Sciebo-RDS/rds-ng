<script setup lang="ts">
import Button from "primevue/button";
import OverlayPanel from "primevue/overlaypanel";
import SplitButton from "primevue/splitbutton";
import { useDialog } from "primevue/usedialog";
import { ref } from "vue";
import { ProjectObject, dummyProjectObject } from "./ProjectObjectStore";
import PropertyDialog from "./PropertyDialog.vue";

const dialog = useDialog();
const props = defineProps(["linkedItemActions", "itemId", "projectObjects", "globalObjectStore", "profileId", "projectProfiles", "mode"]);

const object = (props.projectObjects.get(props.itemId) || props.globalObjectStore.get(props.itemId) || dummyProjectObject(props.itemId)) as ProjectObject;

const linkedItemActions = object ? props.linkedItemActions(object.id, object.instanceLabel(props.projectProfiles)) : [];
const emit = defineEmits(["loadObject"]);
function handleClick() {
    if (object["id"] === undefined) {
        return;
    }
    if (props.mode == "dialog") {
        emit("loadObject", object["id"]);
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
                modal: true
            },
            data: {
                id: object["id"],
                projectObjectStore: props.projectObjects,
                globalObjectStore: props.globalObjectStore,
                propertyProfileStore: props.projectProfiles,
                profileId: props.profileId
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
    <div>
        <SplitButton
            v-if="object.type !== 'dummy'"
            menuButtonIcon="pi pi-ellipsis-v"
            :model="linkedItemActions"
            menuitemicon="pi pi-link"
            @click="
                () => {
                    object === undefined ? null : handleClick();
                }
            "
            :style="`--p-color: ${object.bgColor(props.projectProfiles)}; --p-border-color: ${object.borderColor(props.projectProfiles)};`"
        >
            <span class="text-lg mx-2 truncate">
                {{ props.projectProfiles.getLabelById(object["type"]) }}: {{ object.instanceLabel(props.projectProfiles) }}
            </span>
        </SplitButton>
        <Button
            v-else
            menuButtonIcon="pi pi-ellipsis-v"
            :model="linkedItemActions"
            menuitemicon="pi pi-link"
            :style="`background-color: ${object.bgColor(props.projectProfiles)}; border-color: ${object.borderColor(props.projectProfiles)}; height: 2rem`"
            class="text-gray-600"
            @click="toggle"
        >
            <i class="pi pi-exclamation-circle mx-1" style="color: #ee0000" />
            <span class="text-lg mx-2 truncate"> {{ "broken link" }}: {{ object.instanceLabel(props.projectProfiles) }} </span>
        </Button>

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
                                props.globalObjectStore.remove(props.itemId, props.itemId);
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
