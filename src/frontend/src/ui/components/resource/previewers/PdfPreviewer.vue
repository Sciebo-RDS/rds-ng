<script setup lang="ts">
import { onMounted, type PropType, ref, toRefs, unref } from "vue";

import { Resource } from "@common/data/entities/resource/Resource";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useResourceTools } from "@/ui/tools/resource/ResourceTools";
import MiniPreview from "../MiniPreview.vue";
import PreviewOverlay from "../PreviewOverlay.vue";

const comp = FrontendComponent.inject();
const props = defineProps({
    resource: {
        type: Object as PropType<Resource>,
        required: true
    }
});
const { resource } = toRefs(props);

const pdfData = ref("");

onMounted(() => {
    const { retrieveResourceData, resourceDataToTagValue } = useResourceTools(comp);

    retrieveResourceData(unref(resource)!).then((data: string) => {
        pdfData.value = resourceDataToTagValue(unref(resource)!, data);
    });
});

const previewVisible = ref(false);
</script>

<template>
    <div @click="() => (!!pdfData ? (previewVisible = true) : '')">
        <MiniPreview :loading="!pdfData" icon="pi-search">
            <template #preview>
                <object :data="pdfData" :type="resource.mime_type" style="pointer-events: none" class="h-[calc(12rem-0.5rem)] rounded"></object>
            </template>
        </MiniPreview>

        <PreviewOverlay v-if="previewVisible" @close="previewVisible = false" :header="resource.filename">
            <object :data="pdfData" :type="resource.mime_type" class="w-full h-screen z-50"></object>
        </PreviewOverlay>
    </div>
</template>

<style scoped lang="scss"></style>
