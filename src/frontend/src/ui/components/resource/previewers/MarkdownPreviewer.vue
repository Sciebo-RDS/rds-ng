<script setup lang="ts">
// @ts-ignore
import markdownit from "markdown-it";

import { onMounted, type PropType, ref, toRefs, unref } from "vue";

import { Resource } from "@common/data/entities/resource/Resource";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useResourceTools } from "@/ui/tools/resource/ResourceTools";
import MiniPreview from "../MiniPreview.vue";
import PreviewOverlay from "../PreviewOverlay.vue";

const md = markdownit();

const comp = FrontendComponent.inject();
const props = defineProps({
    resource: {
        type: Object as PropType<Resource>,
        required: true
    }
});
const { resource } = toRefs(props);

const textData = ref("");
const parsedText = ref("");

onMounted(() => {
    const { retrieveResourceData } = useResourceTools(comp);

    retrieveResourceData(unref(resource)!).then((data: ArrayBuffer | undefined) => {
        const decoder = new TextDecoder();
        const text = decoder.decode(data);

        textData.value = text;
        parsedText.value = md.render(text);
    });
});

const previewVisible = ref(false);
</script>

<template>
    <div @click="() => (!!textData ? (previewVisible = true) : '')">
        <MiniPreview :loading="!textData" icon="pi-search">
            <template #preview>
                <div v-if="!!textData" :innerText="textData" class="overflow-hidden !h-[calc(12rem-0.5rem)] whitespace-pre-wrap break-all p-2 font-mono" />
            </template>
        </MiniPreview>

        <PreviewOverlay v-if="previewVisible" @close="previewVisible = false" :header="resource.filename">
            <article :innerHTML="parsedText" class="p-10 prose min-w-[100%] overflow-auto w-full bg-white"></article>
        </PreviewOverlay>
    </div>
</template>

<style scoped lang="scss"></style>
