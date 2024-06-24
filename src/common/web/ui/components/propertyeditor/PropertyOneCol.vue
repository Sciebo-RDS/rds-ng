<script setup lang="ts">
import { FrontendComponent } from "@/component/FrontendComponent";
import Button from "primevue/button";
import { computed, ref, watch, type PropType, type Ref } from "vue";
import LinkedItemButton from "./LinkedItemButton.vue";
import NewPropertyButton from "./NewPropertyButton.vue";
import { ProfileClass, PropertyDataType, propertyDataForms, type ProfileID } from "./PropertyProfile";
import { PropertyProfileStore } from "./PropertyProfileStore";

import { confirmDialog } from "@common/ui/dialogs/ConfirmDialog";
import Chip from "primevue/chip";
import OverlayPanel from "primevue/overlaypanel";
import { ProjectObject, ProjectObjectStore } from "./ProjectObjectStore";

const comp = FrontendComponent.inject();

const emit = defineEmits(["hide"]);
const { propertyClass, profileId, projectObjects, projectProfiles, globalObjectStore } = defineProps({
    propertyClass: {
        type: Object as PropType<ProfileClass>,
        required: true
    },
    profileId: {
        type: Object as PropType<ProfileID>,
        required: true
    },
    projectObjects: {
        type: ProjectObjectStore,
        required: true
    },
    projectProfiles: {
        type: PropertyProfileStore,
        required: true
    },
    globalObjectStore: {
        type: Object as PropType<ProjectObjectStore>,
        required: true
    }
});

projectObjects.add(new ProjectObject(profileId, null, propertyClass.id));

const propertyObject = computed(
    () => projectObjects.get(propertyClass.id) || projectObjects.add(new ProjectObject(profileId, null, propertyClass.id))
) as Ref<ProjectObject>;

watch(
    () => projectObjects.get(propertyClass.id),
    (obj) => {
        if (!obj) projectObjects.add(new ProjectObject(profileId, null, propertyClass.id));
    }
);

const op = ref();
const toggle = (event: Event) => {
    op.value.toggle(event);
};

const example = propertyClass.example ? `<b>Example</b>: ${propertyClass.example}` : null;

//make this global with linkedItemActions in PropertyDialog.vue
const linkedItemActions = ref((id: string, label: Ref<string>) => [
    {
        label: "Unlink",
        icon: "pi pi-minus",
        command: () => {
            confirmDialog(comp, {
                header: `Unlink "${label.value}?"`,
                message: "Are you sure you want to unlink this property? The object will not be deleted, you can relink at any time.",
                acceptLabel: "Unlink",
                acceptIcon: "pi pi-minus",
                acceptClass: "p-button-danger",
                rejectLabel: "Cancel",
                rejectIcon: "pi pi-times",
                rejectClass: "p-button-secondary"
            }).then(() => {
                console.log("Unlinking " + id);
                projectObjects.removeLink(propertyClass.id, id);
            });
        }
    },
    {
        label: "Delete",
        icon: "pi pi-trash",
        command: () => {
            confirmDialog(comp, {
                header: `Delete "${label.value}"?`,
                message: "Are you sure you want to delete this object? It will not be recoverable.",
                acceptLabel: "Delete",
                acceptIcon: "pi pi-trash",
                acceptClass: "p-button-danger",
                rejectLabel: "Cancel",
                rejectIcon: "pi pi-times",
                rejectClass: "p-button-secondary"
            }).then(() => {
                console.log("Deleting " + id);
                projectObjects.remove(id);
            });
        }
    }
]);

const displayableInputs = propertyClass["input"] || [];

const addableTypes = propertyClass["type"];

const linkedObjects = computed(() => projectObjects.getLinkedObjects(propertyClass.id));

const removeLayoutProperty = (propertyClass: ProfileClass) => {
    confirmDialog(comp, {
        header: `Remove "${propertyClass.label}?"`,
        message: `Are you sure you want to remove this property? The data for "${propertyClass.label}" will be lost.`,
        acceptLabel: "Remove",
        acceptIcon: "pi pi-trash",
        acceptClass: "p-button-danger",
        rejectLabel: "Cancel",
        rejectIcon: "pi pi-times",
        rejectClass: "p-button-secondary"
    }).then(() => {
        projectObjects.remove(propertyClass.id);
        emit("hide", propertyClass.id);
    });
};
</script>

<template>
    <div class="flex flex-row <!--hover:bg-gray-100--> p-2 pl-0 rounded group">
        <div>
            <Button
                :disabled="propertyClass.required"
                text
                icon="pi pi-trash"
                :aria-label="'Remove ' + propertyClass.label"
                :title="'Remove ' + propertyClass.label"
                :class="propertyClass.required ? 'invisible' : 'invisible group-hover:visible'"
                class="pt-0"
                @click="removeLayoutProperty(propertyClass)"
                aria-haspopup="true"
                aria-controls="overlay_menu"
                :pt="{ root: { class: 'text-slate-400 hover:text-red-600 bg-transparent' } }"
            />
        </div>
        <div class="grow">
            <!--  Header Row -->
            <div class="row-span-1 text-gray-800 justify-between flex flex-wrap gap-4">
                <span :title="propertyClass.label" class="min-w-fit">
                    <span class="text-xl"> {{ propertyClass.label }}</span>
                    <Button unstyled @click="toggle">
                        <i v-if="propertyClass.description" class="pi pi-question-circle mx-2" style="font-size: 1rem" />
                    </Button>
                    <OverlayPanel ref="op" class="max-w-lg">
                        {{ propertyClass.description }}
                        <p :v-if="propertyClass.example" class="mt-2" v-html="example"></p>
                    </OverlayPanel>
                </span>

                <span class="mr-auto">
                    <NewPropertyButton
                        v-for="t in addableTypes"
                        :key="t"
                        :type="t"
                        :parentId="propertyClass.id"
                        :profileId="profileId"
                        :projectObjects="projectObjects"
                        :globalObjectStore="globalObjectStore as ProjectObjectStore"
                        :projectProfiles="projectProfiles"
                        class="m-1"
                    />
                </span>

                <Chip :label="profileId[0]" size="small" class="bg-[#83d5ff] h-4 !rounded px-2 py-3 text-sm bg-opacity-40 ml-1" />
            </div>
            <!-- <span class="bg-blue-100"> {{ propertyClass }} </span> -->
            <!--  Linked Items Row -->
            <div class="row-span-1 flex my-3 flex-wrap gap-2">
                <LinkedItemButton
                    v-for="i in linkedObjects"
                    :key="i"
                    class="m-1"
                    :profileId="profileId"
                    :linkedItemActions="linkedItemActions"
                    :item="i"
                    :projectObjects="projectObjects"
                    :globalObjectStore="globalObjectStore as ProjectObjectStore"
                    :projectProfiles="projectProfiles"
                />
            </div>
            <!-- Simple Input Row -->
            <div class="space-y-3 mt-5">
                <div v-for="input in displayableInputs" class="row-span-1">
                    <span v-if="input.label !== propertyClass.label">{{ input.label }}</span>
                    <component
                        :is="propertyDataForms[input['type'] as PropertyDataType]"
                        class="w-full"
                        :propertyObjectId="propertyObject['id']"
                        :profileId="profileId"
                        :projectObjects="projectObjects"
                        :globalObjectStore="globalObjectStore as ProjectObjectStore"
                        :inputId="input['id']"
                        :inputOptions="input['options'] ? input['options'] : []"
                    />
                </div>
            </div>
        </div>
    </div>
</template>
