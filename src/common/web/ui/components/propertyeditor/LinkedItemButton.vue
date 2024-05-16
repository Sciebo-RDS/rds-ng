<script setup lang="ts">
import { computed } from "vue";
import PropertyDialog from "./PropertyDialog.vue";
import SplitButton from "primevue/splitbutton";
import { useDialog } from "primevue/usedialog";
import { ProjectObject, ProjectObjectStore } from "./ProjectObjectStore";
import { injectTemplate } from "./utils/Templates";

const dialog = useDialog();
const props = defineProps(["linkedItemActions", "item", "projectObjects", "profileId", "projectProfiles", "mode"]);

const object = props.projectObjects.get(props.item);

const linkedItemActions = props.linkedItemActions(object.id);

const emit = defineEmits(["loadObject"]);

const label = computed(() => {
    const injectedLabel = injectTemplate(props.projectProfiles.getClassById(object.profile, object.type).labelTemplate, props.projectObjects.get(object.id));
    return `${object.type}: ${injectedLabel}`;
});

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
    >
        <span class="text-lg mx-2 truncate"> {{ label }} </span>
    </SplitButton>
</template>

<style scoped lang="scss">
.p-splitbutton {
    @apply h-8 text-gray-600 border border-[#787878];
}
:deep(.p-splitbutton-defaultbutton) {
    @apply bg-[#ffdc83] bg-opacity-30	 border-0 px-2 text-inherit;
}

:deep(.p-splitbutton-menubutton) {
    @apply bg-[#ffdc83] bg-opacity-50	 border-0 border-l border-[#787878] text-inherit;
}
</style>
