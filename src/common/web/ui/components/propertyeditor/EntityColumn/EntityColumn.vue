<script setup lang="ts">
import type { ProfileClassRef } from "../PropertyProfile";

import EntityColumnHeader from "./EntityColumnHeader.vue";
import EntityColumnInputs from "./EntityColumnInputs.vue";
import EntityColumnLinkedItems from "./EntityColumnLinkedItems.vue";

const props = defineProps(["propertyClass", "profiles", "projectProfiles", "sharedPropertyObjectStore", "propertyObjects", "propertyObject"]);

const displayableInputs = props.propertyClass.getInputs();

const addableTypes = props.propertyClass.getRefTypes() as ProfileClassRef[];
</script>

<template>
    <div class="w-full grid grid-cols-1 space-y-2">
        <!--  Header Row -->
        <EntityColumnHeader
            :addableTypes="addableTypes"
            :propertyClass="propertyClass"
            :propertyObject="propertyObject"
            :propertyObjects="propertyObjects"
            :sharedPropertyObjectStore="sharedPropertyObjectStore"
            :projectProfiles="projectProfiles"
            :profiles="profiles"
        />

        <!--  Linked Items Row -->

        <EntityColumnLinkedItems
            v-if="addableTypes !== undefined && addableTypes.length > 0"
            :propertyObjects="propertyObjects"
            :propertyClass="propertyClass"
            :sharedPropertyObjectStore="sharedPropertyObjectStore"
            :projectProfiles="projectProfiles"
            :addableTypes="addableTypes"
            :propertyObject="propertyObject"
        />

        <!-- Simple Input Rows -->
        <EntityColumnInputs
            v-if="displayableInputs.length > 0"
            class="space-y-2 mt-2"
            :displayableInputs="displayableInputs"
            :propertyObject="propertyObject"
            :propertyObjects="propertyObjects"
            :propertyClass="propertyClass"
        />
    </div>
</template>
