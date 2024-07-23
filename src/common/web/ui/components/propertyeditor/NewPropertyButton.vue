<script setup lang="ts">
import SplitButton from "primevue/splitbutton";
import { useDialog } from "primevue/usedialog";
import { computed } from "vue";
import { SharedObject } from "./ProjectObjectStore";
import PropertyDialog from "./PropertyDialog.vue";
import { injectTemplate } from "./utils/Templates";

const dialog = useDialog();
const props = defineProps(["type", "parentId", "projectObjects", "sharedObjectStore", "projectProfiles", "mode"]);

const emit = defineEmits(["loadObject"]);
const label = props.projectProfiles.getClassLabelById(props.type);
const linkableItems = computed(() => {
    const linkedItems = [...props.projectObjects.getReferencedObjects(props.parentId), ...props.sharedObjectStore.getReferencedObjects(props.parentId)].flat();
    const linkable = props.sharedObjectStore
        .getObjectsByType(props.type)
        .filter((item: SharedObject) => !linkedItems.includes(item.id))
        .filter((item: SharedObject) => item.id != props.parentId);
    return linkable.length > 0
        ? linkable.map((item: SharedObject) => ({
              label: injectTemplate(props.projectProfiles.getLabelTemplateById(item.type), props.sharedObjectStore.get(item.id)),
              command: () => {
                  props.projectObjects.addRef(props.parentId, item.id) || props.sharedObjectStore.addRef(props.parentId, item.id);
              }
          }))
        : [];
});

function createObject() {
    const newObject = new SharedObject(props.type);
    props.sharedObjectStore.add(newObject);
    props.projectObjects.addRef(props.parentId, newObject["id"]) || props.sharedObjectStore.addRef(props.parentId, newObject["id"]);

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
                modal: true,
                dismissableMask: true
            },
            data: {
                id: newObject["id"],
                projectObjects: props.projectObjects,
                sharedObjectStore: props.sharedObjectStore,
                projectProfiles: props.projectProfiles
            }
        });
    }
}
</script>

<template>
    <SplitButton
        @click="() => createObject()"
        @contextmenu="(e: Event) => e.preventDefault()"
        :model="linkableItems.length ? linkableItems : [{ label: `No linkable ${label}(s) available`, disabled: true }]"
    >
        <span :title="'Add new ' + label" class="capitalize text-nowrap">
            <i class="pi pi-plus text-xs capitalize"> </i>
            {{ label }}
        </span>
        <template #menubuttonicon title="test"><i class="pi pi-link" :title="'Link existing ' + label"></i> </template>
    </SplitButton>
</template>

<style scoped lang="scss">
.p-splitbutton {
    @apply h-6 text-gray-600 border border-[#608f00];
}
:deep(.p-splitbutton-defaultbutton) {
    @apply bg-[#eaffbe] bg-opacity-50 border-0 px-2 text-inherit;
}

:deep(.p-splitbutton-menubutton) {
    @apply bg-[#eaffbe] bg-opacity-50 border-0 border-l border-[#608f00] text-inherit;
}
</style>
