<script setup lang="ts">
import PropertySet from "./PropertySet.vue";

import { ProjectObjectStore } from "./ProjectObjectStore";
import { Profile } from "./PropertyProfile";
import { PropertyProfileStore } from "./PropertyProfileStore";

const { projectProfiles } = defineProps({
    projectProfiles: {
        type: PropertyProfileStore,
        required: true
    }
});


const projectObjects = defineModel();
const sharedObjects = defineModel("sharedObjects");


// TODO REMOVE profile prop everywhere
const dummyProfile: Profile = {
    metadata: {
        id: ["none", "0.1"],
        name: "dummy",
        description: "none",
        version: "0.1"
    },
    layout: []
};
</script>

<template>
    <div class="overflow-hidden mr-4">
        <PropertySet
            :profile="dummyProfile"
            :projectObjects="projectObjects as ProjectObjectStore"
            :sharedObjectStore="sharedObjects as ProjectObjectStore"
            :projectProfiles="projectProfiles"
        />
    </div>
</template>
