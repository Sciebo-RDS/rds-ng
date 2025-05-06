<script setup lang="ts">
import EntityComlumnInput from "./EntityColumnInput.vue";

const { displayableInputs, propertyClass, propertyObject, propertyObjects, isDialog } = defineProps([
    "displayableInputs",
    "propertyClass",
    "propertyObject",
    "propertyObjects",
    "isDialog"
]);
</script>
<template>
    <div class="space-y-3">
        <EntityComlumnInput
            v-for="input in displayableInputs"
            :input="input"
            :propertyClass="propertyClass"
            :propertyObject="propertyObject"
            :propertyObjects="propertyObjects"
            :isDialog="isDialog"
            class="row-span-1 space-y-0.5"
        />
    </div>
</template>
