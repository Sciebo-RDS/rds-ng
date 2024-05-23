<script setup lang="ts">
import { computed } from "vue";
import PropertyDialog from "./PropertyDialog.vue";
import SplitButton from "primevue/splitbutton";
import { useDialog } from "primevue/usedialog";
import { ProjectObject, ProjectObjectStore } from "./ProjectObjectStore";
import { injectTemplate } from "./utils/Templates";
import { calculateClassColor } from "./utils/Colors";

const dialog = useDialog();
const props = defineProps(["linkedItemActions", "item", "projectObjects", "profileId", "projectProfiles", "mode"]);

const object = props.projectObjects.get(props.item);

const linkedItemActions = props.linkedItemActions(object.id);

const emit = defineEmits(["loadObject"]);

const objectClass = props.projectProfiles.getClassById(props.profileId, object.type);
const { bgColor, borderColor } = calculateClassColor(props.projectProfiles, props.profileId, object.type, 99, 10);

const injectedLabel = computed(() => injectTemplate(objectClass.labelTemplate, props.projectObjects.get(object.id)));

function handleClick() {
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
            data: { id: object["id"], projectObjectStore: props.projectObjects, propertyProfileStore: props.projectProfiles, profileId: props.profileId }
        });
    }
}
</script>

<template>
    <SplitButton
        menuButtonIcon="pi pi-ellipsis-v"
        :model="linkedItemActions"
        @click="
            () => {
                handleClick();
            }
        "
        :style="`--p-color: ${bgColor}; --p-border-color: ${borderColor};`"
    >
        <span class="text-lg mx-2 truncate"> {{ objectClass.label }}: {{ injectedLabel }} </span>
    </SplitButton>
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
