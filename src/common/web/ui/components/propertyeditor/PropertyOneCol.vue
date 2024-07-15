<script setup lang="ts">
import Button from "primevue/button";
import { computed, ref, watch, type PropType, type Ref } from "vue";
import LinkedItemButton from "./LinkedItemButton.vue";
import NewPropertyButton from "./NewPropertyButton.vue";
import { ProfileClass, PropertyDataType, propertyDataForms, type ProfileID } from "./PropertyProfile";
import { PropertyProfileStore } from "./PropertyProfileStore";
import { stringToColor } from "./utils/Colors";

import Chip from "primevue/chip";
import OverlayPanel from "primevue/overlaypanel";
import { LayoutObject, ProjectObject, ProjectObjectStore } from "./ProjectObjectStore";

const emit = defineEmits(["hide"]);
const { index, propertyClass, profileId, projectObjects, projectProfiles, sharedObjectStore, layoutProfiles } = defineProps({
    index: {
        type: Number,
        required: true
    },
    propertyClass: {
        type: Object as PropType<ProfileClass & { profiles: ProfileID[] }>,
        required: true
    },
    profileId: {
        type: Object as PropType<ProfileID>,
        required: true
    },
    projectObjects: {
        type: Object as PropType<ProjectObjectStore>,
        required: true
    },
    projectProfiles: {
        type: PropertyProfileStore,
        required: true
    },
    sharedObjectStore: {
        type: Object as PropType<ProjectObjectStore>,
        required: true
    },
    layoutProfiles: {
        type: Object as PropType<Array<ProfileClass & { profiles: [] }>>,
        required: true
    }
});

projectObjects.add(new LayoutObject(propertyClass.profiles, propertyClass.id));

const propertyObject = computed(
    () => projectObjects.get(propertyClass.id) || projectObjects.add(new LayoutObject(propertyClass.profiles, propertyClass.id))
) as Ref<ProjectObject>;

watch(
    () => projectObjects.get(propertyClass.id),
    (obj) => {
        if (!obj) projectObjects.add(new LayoutObject(propertyClass.profiles, propertyClass.id));
    }
);

const op = ref();
const toggleRemoveDeadLink = (event: Event) => {
    op.value.toggle(event);
};

const displayableInputs = propertyClass["input"] || [];

const addableTypes = propertyClass["type"];

const linkedObjects = computed(() => projectObjects.getReferencedObjects(propertyClass.id));

const profiles = layoutProfiles?.find((e) => e.id == propertyObject.value.id)!.profiles as ProfileID[];

const removeProperty = ref();
const toggleRemoveProperty = (e: Event) => {
    removeProperty.value.toggle(e);
};
</script>

<template>
    <div class="flex flex-row <!--hover:bg-gray-100--> px-2 pl-0 rounded group max-w-full w-full">
        <div class="grid w-16 justify-center shrink-0">
            <div class="text-gray-400 mt-0 pt-0 text-lg ml-auto mr-2" :class="propertyClass.required ? '' : 'group-hover:hidden'">{{ index + 1 }}.</div>
            <OverlayPanel ref="removeProperty" class="py-2 px-5">
                <div class="flex flex-col gap-4">
                    <h3 class="text-lg font-bold">Remove "{{ propertyClass.label }}"?</h3>
                    <p>The data for property "{{ propertyClass.label }}" will be lost.</p>
                    <div class="flex gap-2 ml-auto">
                        <Button
                            severity="danger"
                            @click="
                                () => {
                                    projectObjects.remove(propertyClass.id);
                                    emit('hide', propertyClass.id);
                                }
                            "
                        >
                            Delete
                        </Button>
                        <Button
                            outlined
                            @click="
                                (e) => {
                                    toggleRemoveProperty(e);
                                }
                            "
                            >Cancel</Button
                        >
                    </div>
                </div>
            </OverlayPanel>
            <Button
                :disabled="propertyClass.required"
                text
                icon="pi pi-trash"
                :aria-label="'Remove ' + propertyClass.label"
                :title="'Remove ' + propertyClass.label"
                :class="propertyClass.required ? 'invisible' : 'invisible group-hover:visible'"
                class="pt-0 mt-0 h-9"
                @click="toggleRemoveProperty($event)"
                :pt="{ root: { class: 'text-gray-400 hover:text-red-600 bg-transparent' } }"
            />
        </div>
        <div class="w-full grid grid-cols-1">
            <!--  Header Row -->
            <div class="row-span-1 text-gray-800 justify-between flex flex-wrap gap-4 max-w-full w-full">
                <span :title="propertyClass.label" class="min-w-fit">
                    <span class="text-lg"> {{ propertyClass.label }} </span>
                    <Button v-if="propertyClass.description" unstyled @click="toggleRemoveDeadLink">
                        <i class="pi pi-question-circle mx-2" style="font-size: 1rem; color: gray" /> </Button
                    ><!-- <span v-if="propertyClass.required" class="text-red-500">*</span> -->
                    <OverlayPanel ref="op" class="max-w-lg">
                        {{ propertyClass.description }}
                        <p v-if="propertyClass.example" class="mt-2" v-html="`<b>Example</b>: ${propertyClass.example}`" />
                    </OverlayPanel>
                </span>
                <span class="mr-auto gap-1">
                    <NewPropertyButton
                        v-for="t in addableTypes"
                        :key="t"
                        :type="t"
                        :parentId="propertyObject['id']"
                        :profileId="profileId"
                        :projectObjects="projectObjects"
                        :sharedObjectStore="sharedObjectStore as ProjectObjectStore"
                        :projectProfiles="projectProfiles"
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
            <div
                v-if="addableTypes !== undefined && addableTypes.length > 0"
                class="row-span-1 flex mt-3 p-2 flex-wrap gap-0.5 rounded-md border"
                style="
                    box-shadow:
                        0 0 #0000,
                        0 0 #0000,
                        0 1px 2px 0 rgba(18, 18, 23, 0.05);
                    transition:
                        background-color 0.2s,
                        color 0.2s,
                        border-color 0.2s,
                        box-shadow 0.2s,
                        outline-color 0.2s;
                    border: 1px dashed #b6bfca;
                "
            >
                <LinkedItemButton
                    v-if="linkedObjects.length > 0"
                    v-for="i in linkedObjects"
                    :key="i"
                    class="m-1 max-w-full"
                    :profileId="profileId"
                    :item-id="i"
                    :parentId="propertyClass.id"
                    :projectObjects="projectObjects"
                    :sharedObjectStore="sharedObjectStore as ProjectObjectStore"
                    :projectProfiles="projectProfiles"
                />
                <span v-else class="text-gray-500 m-1 my-3 place-self-center align-middle inline-block">No {{ addableTypes.join(" / ") }} linked</span>
            </div>
            <!-- Simple Input Row -->
            <div v-if="displayableInputs.length > 0" class="space-y-2 mt-2">
                <div v-for="input in displayableInputs" class="row-span-1">
                    <span v-if="input.label !== propertyClass.label">{{ input.label }}</span>
                    <component
                        :is="propertyDataForms[input['type'] as PropertyDataType]"
                        class="w-full"
                        :propertyObjectId="propertyObject['id']"
                        :profileId="profileId"
                        :projectObjects="projectObjects"
                        :inputId="input['id']"
                        :inputOptions="input['options'] ? input['options'] : []"
                    />
                </div>
            </div>
        </div>
    </div>
</template>
