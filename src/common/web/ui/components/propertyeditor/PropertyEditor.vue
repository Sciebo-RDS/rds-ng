<script setup lang="ts">
import { reactive, watch } from "vue";
import PropertySet from "./PropertySet.vue";

import { PropertyObject, PropertyObjectStore, SharedPropertyObject } from "./PropertyObjectStore";
import { PropertyProfileStore } from "./PropertyProfileStore";

const { projectProfiles, showProfileTags } = defineProps({
    projectProfiles: {
        type: PropertyProfileStore,
        required: true
    },
    showProfileTags: {
        type: Boolean,
        default: true
    }
});

const propertyObjects = reactive(new PropertyObjectStore());
const sharedPropertyObjectStore = reactive(new PropertyObjectStore());
const metadata = defineModel();
propertyObjects.setObjects((metadata.value as PropertyObject[]) || []);
watch(
    () => metadata.value,
    () => propertyObjects.setObjects(metadata.value as PropertyObject[])
);
watch(
    () => propertyObjects.exportObjects(),
    () => {
        metadata.value = propertyObjects.exportObjects();
    }
);
const sharedPropertyObjects = defineModel("sharedPropertyObjects");
sharedPropertyObjectStore.setObjects((sharedPropertyObjects.value as SharedPropertyObject[]) || []);
watch(
    () => sharedPropertyObjects.value,
    () => sharedPropertyObjectStore.setObjects(sharedPropertyObjects.value as SharedPropertyObject[])
);
watch(
    () => sharedPropertyObjectStore.exportObjects(),
    () => (sharedPropertyObjects.value = sharedPropertyObjectStore.exportObjects())
);
</script>

<template>
    <div class="overflow-hidden mr-4">
        <PropertySet
            :propertyObjects="propertyObjects as PropertyObjectStore"
            :sharedPropertyObjectStore="sharedPropertyObjectStore as PropertyObjectStore"
            :projectProfiles="projectProfiles"
            :show-profile-tags="showProfileTags"
        />
    </div>
</template>
