<script setup lang="ts">
import { watch, type PropType } from "vue";
import PropertySet from "./PropertySet.vue";

import { ProjectObject, ProjectObjectStore } from "./ProjectObjectStore";
import { Profile } from "./PropertyProfile";
import { PropertyProfileStore } from "./PropertyProfileStore";

const { projectProfiles, projectObjects, globalObjectStore } = defineProps({
    projectProfiles: {
        type: PropertyProfileStore,
        required: true
    },
    projectObjects: {
        type: ProjectObjectStore,
        required: true
    },
    globalObjectStore: {
        type: Object as PropType<ProjectObjectStore>,
        required: true
    }
});

const model = defineModel();
projectObjects.setObjects(model.value as ProjectObject[]);

watch(
    () => model.value,
    () => projectObjects.setObjects(model.value as ProjectObject[])
);

watch(
    () => projectObjects.exportObjects(),
    () => (model.value = projectObjects.exportObjects())
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
