<script setup lang="ts">
import { ref, inject, computed, unref } from "vue";
import { propertyDataForms, type Property } from "./PropertyProfile";
import Button from "primevue/button";
import NewPropertyButton from "./NewPropertyButton.vue";
import LinkedItemButton from "./LinkedItemButton.vue";
import { PropertyDataType } from "./PropertyProfile";
import { PropertyProfileStore } from "./PropertyProfileStore";

import OverlayPanel from "primevue/overlaypanel";
import Chip from "primevue/chip";
import Skeleton from "primevue/skeleton";
import { ProjectObject, type ProjectObjectStore } from "./ProjectObjectStore";

const emit = defineEmits(["hide"]);
const props = defineProps(["propertyClass", "profileId", "projectObjects", "propertyObject", "projectProfiles"]);

if ((props.propertyClass === props.propertyObject) === undefined) {
    throw new Error("PropertyOneCol: propertyClass or propertyObject must be defined");
}
const profileId = props.profileId as string;

const propertyClass = props.propertyClass ? props.propertyClass : props.projectProfiles.getClassById(profileId, props.propertyObject["type"]); // get propertyClass by propertyObject.type
let propertyObject = props.propertyObject
    ? props.propertyObject
    : props.projectObjects.add(new ProjectObject(profileId, propertyClass["type"], propertyClass.id));

propertyObject = computed(() => props.projectObjects.get(propertyClass.id));

const op = ref();
const toggle = (event: Event) => {
    op.value.toggle(event);
};

const example = propertyClass.example ? `<b>Example</b>: ${propertyClass.example}` : null;

const linkedItemActions = ref((id: string) => [
    {
        label: "Unlink",
        icon: "pi pi-minus",
        command: () => {
            console.log("Unlinking " + id);
            props.projectObjects.removeLink(propertyClass.id, id);
        }
    },
    {
        label: "Delete",
        icon: "pi pi-trash",
        command: () => {
            console.log("Deleting " + id);
            props.projectObjects.remove(id);
        }
    }
]);

const displayableInputs = propertyClass["input"] || [];

const addableTypes = propertyClass["type"] || [];

const linkedObjects = computed(() => props.projectObjects.getLinkedObjects(propertyClass.id));

const removeProperty = (id: string) => {
    props.projectObjects.remove(id);
    emit("hide", id);
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
                @click="removeProperty(propertyClass.id)"
                aria-haspopup="true"
                aria-controls="overlay_menu"
                :pt="{ root: { class: 'text-slate-400 hover:text-red-600 bg-transparent' } }"
            />
        </div>
        <div class="grow">
            <!--  Header Row -->
            <div class="row-span-1 text-gray-800 justify-between flex items-center">
                <span :title="propertyClass.label">
                    <span class="text-xl"> {{ propertyClass.label }}</span>
                    <Button unstyled @click="toggle">
                        <i v-if="propertyClass.description" class="pi pi-question-circle mx-2" style="font-size: 1rem" />
                    </Button>
                    <OverlayPanel ref="op" class="max-w-lg">
                        {{ propertyClass.description }}
                        <p :v-if="propertyClass.example" class="mt-2" v-html="example"></p>
                    </OverlayPanel>
                </span>

                <span class="mr-auto ml-5 flex space-x-1">
                    <NewPropertyButton
                        v-for="t in addableTypes"
                        v-if="linkedObjects.length > 0"
                        :key="t['id']"
                        :type="t"
                        :parentId="propertyClass.id"
                        :profileId="profileId"
                        :projectObjects="projectObjects"
                        :projectProfiles="projectProfiles"
                    />
                </span>

                <Chip label="$RepoLabel" size="small" class="bg-[#83d5ff] h-4 !rounded px-2 py-3 text-sm bg-opacity-40" />
            </div>
            <!--             <span class="bg-blue-100">
                {{ propertyObject }}
            </span> -->
            <!--  Linked Items Row -->
            <div class="row-span-1 flex mt-3 flex-wrap">
                <LinkedItemButton
                    v-for="i in linkedObjects"
                    v-if="linkedObjects?.length !== 0"
                    :key="i"
                    class="m-1"
                    :profileId="profileId"
                    :linkedItemActions="linkedItemActions"
                    :item="i"
                    :projectObjects="projectObjects"
                    :projectProfiles="projectProfiles"
                />
                <NewPropertyButton
                    v-for="t in addableTypes"
                    v-else
                    :key="t['id']"
                    :type="t"
                    :parentId="propertyClass.id"
                    :profileId="profileId"
                    :projectObjects="projectObjects"
                    :projectProfiles="projectProfiles"
                />
            </div>
            <!-- Simple Input Row -->
            <div class="space-y-3">
                <div v-for="input in displayableInputs" class="row-span-1">
                    <span v-if="input.label !== propertyClass.label">{{ input.label }}</span>
                    <component
                        :is="propertyDataForms[input['type'] as PropertyDataType]"
                        class="w-full"
                        :propertyObjectId="propertyObject['id']"
                        :profileId="profileId"
                        :projectObjects="projectObjects"
                        :inputId="input['id']"
                    />
                </div>
            </div>
        </div>
    </div>
</template>
