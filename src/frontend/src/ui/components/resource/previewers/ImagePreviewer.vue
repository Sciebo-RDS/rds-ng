<script setup lang="ts">
import Image from "primevue/image";
import Skeleton from "primevue/skeleton";
import { onMounted, type PropType, ref, toRefs, unref } from "vue";

import { Resource } from "@common/data/entities/resource/Resource";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useResourceTools } from "@/ui/tools/resource/ResourceTools";

const comp = FrontendComponent.inject();
const props = defineProps({
    resource: {
        type: Object as PropType<Resource>,
        required: true
    }
});
const { resource } = toRefs(props);

const imageData = ref("");

onMounted(() => {
    const { retrieveResourceData, resourceDataToTagValue } = useResourceTools(comp);

    retrieveResourceData(unref(resource)!).then((data: string) => {
        imageData.value = resourceDataToTagValue(unref(resource)!, data);
    });
});
</script>

<template>
    <div class="r-centered-grid content-center">
        <Image
            v-if="!!imageData"
            :src="imageData"
            alt="Preview"
            :title="resource.filename"
            preview
            :pt="{ image: 'max-h-[calc(12rem-0.5rem)] rounded' }"
            class="rounded"
        >
            <template #indicatoricon>
                <i class="pi pi-search"></i>
            </template>
        </Image>
        <Skeleton v-else title="Loading image..." class="!w-[calc(12rem-0.5rem)] !h-[calc(12rem-0.5rem)]"></Skeleton>
    </div>
</template>

<style scoped lang="scss">
:deep(.p-image-preview-indicator) {
    @apply rounded;
}
</style>
