<script setup lang="ts">
import Image from "primevue/image";
import { computed, type PropType, toRefs, unref, watch } from "vue";

import { Resource, ResourceType } from "@common/data/entities/resource/Resource";

import previewImage from "@assets/img/preview.png";

const props = defineProps({
    resources: {
        type: Object as PropType<Resource[]>,
        required: true,
    },
});
const { resources } = toRefs(props);

const noPreview = computed(() => {
    // TODO: Unsupported file types
    return unref(resources)!.length > 1;
});
const isFolder = computed(() => {
    if (unref(resources)!.length == 1) {
        return unref(resources)![0].type == ResourceType.Folder;
    }
    return false;
});

watch(resources, (data) => console.log(data));
</script>

<template>
    <div class="!w-48 !h-48 border rounded-xl">
        <div v-if="noPreview" title="No preview available" class="w-full h-full r-centered-grid content-center r-text-light-gray p-2">
            <span class="material-icons-outlined mi-preview !text-7xl" />
            <p class="w-full text-center">No preview available</p>
        </div>
        <div v-else-if="isFolder" :title="resources[0].filename" class="w-full h-full r-centered-grid content-center r-text-light-gray p-2">
            <span class="material-icons-outlined mi-folder !text-7xl" />
            <p class="w-full text-center truncate">{{ resources[0].filename }}</p>
        </div>
        <Image v-else :src="previewImage" alt="Preview" :title="resources[0].filename" class="w-full h-full" preview />
    </div>
</template>

<style scoped lang="scss"></style>
