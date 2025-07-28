<script setup lang="ts">
import { ref } from "vue";

import Button from "primevue/button";
import Chip from "primevue/chip";
import Popover from "primevue/popover";

import { useColorsStore } from "../../../../data/stores/ColorsStore";
import MandatoryMark from "../../misc/MandatoryMark.vue";
import NewPropertyButton from "../NewPropertyButton.vue";
import type { ProfileClassRef } from "../PropertyProfile";

const colorsStore = useColorsStore();
const props = defineProps([
    "isDialog",
    "addableTypes",
    "propertyClass",
    "propertyObjects",
    "propertyObject",
    "sharedPropertyObjectStore",
    "projectProfiles",
    "profiles",
    "showProfileTag"
]);
const emit = defineEmits(["loadObject"]);

const descriptionPopover = ref();
const toggleDescriptionPopover = (event: Event) => {
    descriptionPopover.value.toggle(event);
};
</script>

<template>
    <div class="row-span-1 text-gray-800 justify-between flex items-center">
        <span :title="propertyClass.getDisplayLabel()" class="min-w-fit flex-none">
            <span :class="isDialog ? 'text-xl' : 'text-lg'"> {{ propertyClass.getDisplayLabel() }} </span>
            <MandatoryMark v-if="propertyClass.isRequired()" class="pl-1" color="red" />

            <Button v-if="propertyClass.getDescription()" unstyled @click="toggleDescriptionPopover" :title="propertyClass.getDescription()">
                <i class="pi pi-question-circle mx-2 text-gray-500 text-base" />
            </Button>
            <Popover ref="descriptionPopover" class="max-w-lg">
                {{ propertyClass.getDescription() }}
                <p v-if="propertyClass.getExample()" class="mt-2" v-html="`<b>Example</b>: ${propertyClass.getExample()}`" />
            </Popover>
        </span>
        <span class="mr-auto ml-5 flex gap-1 flex-wrap">
            <NewPropertyButton
                v-for="t in addableTypes.filter((t: ProfileClassRef) => !t.isInline())"
                :key="t.getClassId()"
                :type="t.getClassId()"
                :parentId="propertyObject.getId()"
                :propertyObjects="propertyObjects"
                :sharedPropertyObjectStore="sharedPropertyObjectStore"
                :projectProfiles="projectProfiles"
                :isDialog="isDialog"
                @loadObject="(id) => emit('loadObject', id)"
            />
        </span>
        <span v-if="showProfileTag" class="flex self-center gap-2">
            <Chip
                v-for="p in profiles.sort()"
                :label="projectProfiles.getProfileLabelById(p)"
                size="small"
                class="h-4 !rounded py-3 text-sm bg-opacity-40"
                :style="`background-color: ${colorsStore.color(p[0])}`"
            />
        </span>
    </div>
</template>
