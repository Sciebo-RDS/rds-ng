<script setup lang="ts">
import { computed } from "vue";

import LinkedItemButton from "../LinkedItemButton.vue";
import { ProfileClassRef } from "../PropertyProfile";

const emit = defineEmits(["loadObject"]);
const props = defineProps(["propertyObjects", "propertyClass", "addableTypes", "projectProfiles", "sharedPropertyObjectStore", "isDialog"]);
const linkedObjects = computed(() => [
    ...props.sharedPropertyObjectStore.getReferencedObjects(props.propertyClass.getId()),
    ...props.propertyObjects.getReferencedObjects(props.propertyClass.getId())
]);
const addableTypesStr = props.addableTypes
    .map((e: ProfileClassRef) => props.projectProfiles.getClassLabelById(e.getClassId()))
    .join(", ")
    .replace(/, ([^,]*)$/, " or $1");
</script>

<template>
    <div class="row-span-1 flex p-2 flex-wrap gap-0.5 rounded-md border linked-items-box">
        <LinkedItemButton
            v-if="linkedObjects.length > 0"
            v-for="i in linkedObjects"
            :key="i"
            class="m-1 max-w-full"
            :item-id="i"
            :parentId="propertyClass.getId()"
            :propertyObjects="propertyObjects"
            :sharedPropertyObjectStore="sharedPropertyObjectStore"
            :projectProfiles="projectProfiles"
            :isDialog="isDialog"
            @load-object="(id) => emit('loadObject', id)"
        />
        <div v-else class="text-gray-500 m-1 my-3 place-self-center align-middle inline-block">
            No
            <span class="italic">
                {{ addableTypesStr }}
            </span>
            linked
        </div>
    </div>
</template>

<style lang="css" scoped>
.linked-items-box {
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
}
</style>
