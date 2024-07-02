<script setup lang="ts">
import SplitButton from "primevue/splitbutton";
import { useDialog } from "primevue/usedialog";
import { computed } from "vue";
import { ProjectObject } from "./ProjectObjectStore";
import PropertyDialog from "./PropertyDialog.vue";
import { injectTemplate } from "./utils/Templates";

const dialog = useDialog();
const props = defineProps(["type", "profileId", "parentId", "projectObjects", "globalObjectStore", "projectProfiles", "mode"]);

const emit = defineEmits(["loadObject"]);
const label = props.projectProfiles.getClassLabelById(props.type);
const linkableItems = computed(() => {
    const linkedItems = [...props.projectObjects.getLinkedObjects(props.parentId), ...props.globalObjectStore.getLinkedObjects(props.parentId)].flat();
    const linkable = props.globalObjectStore
        .getObjectsByType(props.type)
        .filter((item: ProjectObject) => !linkedItems.includes(item.id))
        .filter((item: ProjectObject) => item.id != props.parentId);
    return linkable.length > 0
        ? linkable.map((item: ProjectObject) => ({
              label: injectTemplate(props.projectProfiles.getLabelTemplateById(item.type), props.globalObjectStore.get(item.id)),
              command: () => {
                  props.projectObjects.addLink(props.parentId, item.id) || props.globalObjectStore.addLink(props.parentId, item.id);
              }
          }))
        : [];
});

function createObject() {
    const newObject = new ProjectObject(props.profileId, props.type);
    props.globalObjectStore.add(newObject);
    props.projectObjects.addLink(props.parentId, newObject["id"]) || props.globalObjectStore.addLink(props.parentId, newObject["id"]);

    if (props.mode == "dialog") {
        emit("loadObject", newObject["id"]);
    } else {
        dialog.open(PropertyDialog, {
            props: {
                header: "New Property",
                style: {
                    "min-width": "50vw",
                    "max-width": "50vw",
                    height: "80vh"
                },
                breakpoints: {
                    "960px": "75vw",
                    "640px": "90vw"
                },
                modal: true
            },
            data: {
                id: newObject["id"],
                projectObjects: props.projectObjects,
                globalObjectStore: props.globalObjectStore,
                projectProfiles: props.projectProfiles,
                profileId: props.profileId
            }
        });
    }
}
</script>

<template>
    <SplitButton
        @click="() => createObject()"
        :model="linkableItems.length ? linkableItems : [{ label: `No linkable ${props.type}(s) available`, disabled: true }]"
    >
        <span :title="'Add new ' + type" class="capitalize text-nowrap">
            <i class="pi pi-plus text-xs capitalize"> </i>
            {{ label }}
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
