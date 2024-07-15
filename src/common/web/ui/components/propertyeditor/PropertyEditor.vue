<script setup lang="ts">
import PropertySet from "./PropertySet.vue";

import { ProjectObjectStore } from "./ProjectObjectStore";
import { PropertyProfileStore } from "./PropertyProfileStore";

const { projectProfiles } = defineProps({
    projectProfiles: {
        type: PropertyProfileStore,
        required: true
    }
});

const projectObjects = defineModel();
const sharedObjects = defineModel("sharedObjects");
</script>

<template>
    <div class="overflow-hidden mr-4">
        <PropertySet
            :projectObjects="projectObjects as ProjectObjectStore"
            :sharedObjectStore="sharedObjects as ProjectObjectStore"
            :projectProfiles="projectProfiles"
        />
    </div>
</template>
