<script setup lang="ts">
import { reactive, watch } from "vue";
import PropertySet from "./PropertySet.vue";

import { ProjectObject, ProjectObjectStore } from "./ProjectObjectStore";
import { PropertyProfileStore } from "./PropertyProfileStore";

const { projectProfiles } = defineProps({
    projectProfiles: {
        type: PropertyProfileStore,
        required: true
    }
});

const projectObjects = reactive(new ProjectObjectStore());
const sharedObjectStore = reactive(new ProjectObjectStore());
const metadata = defineModel();
projectObjects.setObjects((metadata.value as ProjectObject[]) || []);
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
sharedObjectStore.setObjects((sharedObjects.value as ProjectObject[]) || []);
watch(
    () => sharedObjects.value,
    () => sharedObjectStore.setObjects(sharedObjects.value as ProjectObject[])
);
watch(
    () => sharedObjectStore.exportObjects(),
    () => (sharedObjects.value = sharedObjectStore.exportObjects())
);
</script>

<template>
    <div class="overflow-hidden mr-4">
        <PropertySet
            :projectObjects="projectObjects as ProjectObjectStore"
            :sharedObjectStore="sharedObjectStore as ProjectObjectStore"
            :projectProfiles="projectProfiles"
        />
    </div>
</template>
