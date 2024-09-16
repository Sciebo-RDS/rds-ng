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

const textData = ref("");

onMounted(() => {
    const { retrieveResourceData } = useResourceTools(comp);

    retrieveResourceData(unref(resource)!).then((data: ArrayBuffer | undefined) => {
        const decoder = new TextDecoder();
        textData.value = decoder.decode(data);
    });
});

const previewVisible = ref(false);
</script>

<template>
    <div @click="() => (!!textData ? (previewVisible = true) : '')">
        <MiniPreview :loading="!textData" icon="pi-search">
            <template #preview>
                <div v-if="!!textData" :innerText="textData" class="!h-[calc(12rem-0.5rem)] overflow-hidden whitespace-pre-wrap break-all p-2 font-mono" />
            </template>
        </MiniPreview>

        <PreviewOverlay v-if="previewVisible" @close="previewVisible = false" :header="resource.filename">
            <div v-if="!!textData" :innerHTML="textData" class="p-5 overflow-auto bg-white whitespace-pre-wrap break-all font-mono" />
        </PreviewOverlay>
    </div>
</template>

<style scoped lang="scss"></style>
