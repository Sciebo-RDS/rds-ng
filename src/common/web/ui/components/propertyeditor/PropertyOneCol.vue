<script setup lang="ts">
import { FrontendComponent } from "@/component/FrontendComponent";
import Button from "primevue/button";
import { computed, ref, watch, type PropType, type Ref } from "vue";
import LinkedItemButton from "./LinkedItemButton.vue";
import NewPropertyButton from "./NewPropertyButton.vue";
import { ProfileClass, PropertyDataType, propertyDataForms, type ProfileID } from "./PropertyProfile";
import { PropertyProfileStore } from "./PropertyProfileStore";
import { stringToColor } from "./utils/Colors";

import { confirmDialog } from "@common/ui/dialogs/ConfirmDialog";
import Chip from "primevue/chip";
import OverlayPanel from "primevue/overlaypanel";
import { ProjectObject, ProjectObjectStore } from "./ProjectObjectStore";

const comp = FrontendComponent.inject();

const emit = defineEmits(["hide"]);
const { propertyClass, profileId, projectObjects, projectProfiles, globalObjectStore, layoutProfiles } = defineProps({
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
    },
    layoutProfiles: {
        type: Array
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

const profiles = layoutProfiles?.find((e) => e.id == propertyObject.value.id).profiles as ProfileID[];
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
                    <Button v-if="propertyClass.description" unstyled @click="toggle">
                        <i class="pi pi-question-circle mx-2" style="font-size: 1rem" />
                    </Button>
                    <OverlayPanel ref="op" class="max-w-lg">
                        {{ propertyClass.description }}
                        <p v-if="propertyClass.example" class="mt-2" v-html="`<b>Example</b>: ${propertyClass.example}`"/>
                    </OverlayPanel>
                </span>

                <span class="mr-auto">
                    <NewPropertyButton
                        v-for="t in addableTypes"
                        :key="t"
                        :type="t"
                        :parentId="propertyObject['id']"
                        :profileId="profileId"
                        :projectObjects="projectObjects"
                        :globalObjectStore="globalObjectStore as ProjectObjectStore"
                        :projectProfiles="projectProfiles"
                        class="m-1"
                    />
                </span>
                <span class="flex self-center gap-2">
                    <Chip
                        v-for="p in profiles.sort()"
                        :label="projectProfiles.getProfileLabelById(p)"
                        size="small"
                        class="h-4 !rounded py-3 text-sm bg-opacity-40"
                        :style="`background-color: ${stringToColor(p[0])}`"
                /></span>
            </div>
            <!--  Linked Items Row -->
            <div class="row-span-1 flex my-3 flex-wrap gap-2">
                <LinkedItemButton
                    v-for="i in linkedObjects"
                    :key="i"
                    class="m-1"
                    :profileId="profileId"
                    :item-id="i"
                    :parentId="propertyClass.id"
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
