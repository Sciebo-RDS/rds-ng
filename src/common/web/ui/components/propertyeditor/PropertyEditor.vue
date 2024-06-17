<script setup lang="ts">
import { watch, type PropType } from "vue";
import PropertySet from "./PropertySet.vue";

import { ProjectObject, ProjectObjectStore } from "./ProjectObjectStore";
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
</script>

<template>
    <div class="overflow-hidden">
        <div v-for="[i, profile] in projectProfiles.list().entries()" :class="i > 0 ? '!mt-5' : ''" class="mx-4 mt-4">
            <PropertySet
                :profile="profile"
                :projectObjects="projectObjects"
                :globalObjectStore="globalObjectStore as ProjectObjectStore"
                :projectProfiles="projectProfiles"
            />
        </div>
    </div>
</template>
