<script setup lang="ts">
import { ref, inject, watch, computed } from "vue";
import { v4 as uuidv4 } from "uuid";
import PropertyDialog from "./PropertyDialog.vue";
import SplitButton from "primevue/splitbutton";
import { useDialog } from "primevue/usedialog";
import { ProjectObject, ProjectObjectStore } from "./ProjectObjectStore";
import { PropertyProfileStore } from "./PropertyProfileStore";

const dialog = useDialog();
const props = defineProps(["type", "profileId", "parentId", "projectObjects", "projectProfiles", "mode"]);

const emit = defineEmits(["loadObject"]);

const linkableItems = computed(() => {
    let linkedItems = props.projectObjects.getLinkedObjects(props.parentId);
    return props.projectObjects
        .getObjectsByType(props.type)
        .filter((item: ProjectObject) => !linkedItems.includes(item.id))
        .filter((item: ProjectObject) => item.id != props.parentId)
        .map((item: ProjectObject) => ({
            label: item.id,
            command: () => {
                props.projectObjects.addLink(props.parentId, item.id);
            }
        }));
});

function handleClick() {
    // TODO let ObjectStore create the id on object creation, return it and use it in the dialog
    const id = uuidv4();
    const newObject = new ProjectObject(props.profileId, props.type, id);
    props.projectObjects.add(newObject);
    props.projectObjects.addLink(props.parentId, id);

    if (props.mode == "dialog") {
        emit("loadObject", id);
    } else {
        dialog.open(PropertyDialog, {
            props: {
                header: "New Property",
                style: {
                    "min-width": "50vw",
                    "max-width": "50vw",
                    "max-height": "80vh"
                },
                breakpoints: {
                    "960px": "75vw",
                    "640px": "90vw"
                },
                modal: true
            },
            data: { id: id, projectObjectStore: props.projectObjects, propertyProfileStore: props.projectProfiles, profileId: props.profileId }
        });
    }
}
</script>

<template>
    <SplitButton
        @click="
            () => {
                handleClick();
            }
        "
        :model="linkableItems.length ? linkableItems : [{ label: `No linkable ${props.type}(s) available`, disabled: true }]"
    >
        <span :title="'Add new ' + type" class="capitalize">
            <i class="pi pi-plus text-xs capitalize"> </i>
            {{ type }}
        </span>
        <template #menubuttonicon title="test"><i class="pi pi-link" title="Link existing property"></i> </template>
    </SplitButton>
</template>

<style scoped lang="scss">
.p-splitbutton {
    @apply h-6 text-gray-600 border border-[#787878];
}
:deep(.p-splitbutton-defaultbutton) {
    @apply bg-[#eaffbe] bg-opacity-50 border-0 px-2 text-inherit;
}

:deep(.p-splitbutton-menubutton) {
    @apply bg-[#eaffbe] bg-opacity-50 border-0 border-l border-[#787878] text-inherit;
}
</style>
