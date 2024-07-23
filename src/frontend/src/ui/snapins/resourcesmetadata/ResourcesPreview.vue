<script setup lang="ts">
import { computed, type PropType, toRefs, unref } from "vue";

import { Resource, ResourceType } from "@common/data/entities/resource/Resource";

import { ResourcePreviewersCatalog } from "@/ui/components/resource/ResourcePreviewersCatalog";

const props = defineProps({
    resources: {
        type: Object as PropType<Resource[]>,
        required: true,
    },
});
const { resources } = toRefs(props);

const resource = computed(() => (unref(resources)!.length == 1 ? unref(resources)![0] : null));
const resourcePreviewer = computed(() => {
    if (!unref(resource)) {
        return null;
    }
    const previewer = ResourcePreviewersCatalog.find(unref(resource)!.mime_type);
    return previewer ? previewer.component : null;
});
</script>

<template>
    <div class="!w-48 !h-48 border rounded-lg">
        <div v-if="!!resource && !!resourcePreviewer" class="w-full h-full r-centered-grid content-center">
            <component :is="resourcePreviewer" :resource="resource!" :title="resource.filename" />
        </div>
        <div
            v-else-if="!!resource && resource.type == ResourceType.Folder"
            :title="resource.filename"
            class="w-full h-full r-centered-grid content-center r-text-light-gray p-2"
        >
            <span class="material-icons-outlined mi-folder !text-7xl" />
            <p class="w-full text-center truncate">{{ resource.filename }}</p>
        </div>
        <div v-else title="No preview available" class="w-full h-full r-centered-grid content-center r-text-light-gray p-2">
            <span class="material-icons-outlined mi-preview !text-7xl" />
            <p class="w-full text-center">No preview available</p>
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
