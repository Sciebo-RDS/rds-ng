<script setup lang="ts">
import { reactive, watch } from "vue";
import PropertySet from "./PropertySet.vue";

import { ProjectObject, ProjectObjectStore } from "./ProjectObjectStore";
import { Profile } from "./PropertyProfile";
import { PropertyProfileStore } from "./PropertyProfileStore";

const { projectProfiles } = defineProps({
    projectProfiles: {
        type: PropertyProfileStore,
        required: true
    }
});

const projectObjects = reactive(new ProjectObjectStore());
const globalObjectStore = reactive(new ProjectObjectStore());

const metadata = defineModel();
projectObjects.setObjects(metadata.value as ProjectObject[]);

watch(
    () => metadata.value,
    () => projectObjects.setObjects(metadata.value as ProjectObject[])
);

watch(
    () => projectObjects.exportObjects(),
    () => {
        metadata.value = projectObjects.exportObjects();
    }
);

const sharedObjects = defineModel("sharedObjects");
globalObjectStore.setObjects((sharedObjects.value as ProjectObject[]) || []);

watch(
    () => sharedObjects.value,
    () => globalObjectStore.setObjects(sharedObjects.value as ProjectObject[])
);

watch(
    () => globalObjectStore.exportObjects(),
    () => (sharedObjects.value = globalObjectStore.exportObjects())
);

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
            :projectObjects="projectObjects"
            :globalObjectStore="globalObjectStore as ProjectObjectStore"
            :projectProfiles="projectProfiles"
        />
    </div>
</template>
