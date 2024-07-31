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

const videoData = ref("");

onMounted(() => {
    const { retrieveResourceData, resourceDataToTagValue } = useResourceTools(comp);

    retrieveResourceData(unref(resource)!).then((data: string) => {
        videoData.value = resourceDataToTagValue(unref(resource)!, data);
    });
});

const previewVisible = ref(false);
</script>

<template>
    <div @click="() => (!!videoData ? (previewVisible = true) : '')">
        <MiniPreview :loading="!videoData" iconAlwaysVisible="true" icon="pi-play-circle" iconSize="1.5">
            <template #preview>
                <video
                    :src="videoData"
                    :type="resource.mime_type"
                    v-if="!!videoData"
                    @click="() => (!!videoData ? (previewVisible = true) : '')"
                    class="max-h-[calc(12rem-0.5rem)] rounded"
                ></video>
            </template>
        </MiniPreview>

        <PreviewOverlay v-if="previewVisible" @close="previewVisible = false" :header="resource.filename">
            <video v-if="!!videoData" controls autoplay>
                <source :src="videoData" :type="resource.mime_type" />
            </video>
        </PreviewOverlay>
    </div>
</template>

<style scoped lang="scss"></style>
