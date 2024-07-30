<script setup lang="ts">
import { onMounted, type PropType, ref, toRefs, unref } from "vue";

import { Resource } from "@common/data/entities/resource/Resource";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useResourceTools } from "@/ui/tools/resource/ResourceTools";
import MiniPreview from "../MiniPreview.vue";
import PreviewOverlay from "../PreviewOverlay.vue";

import markdownit from "markdown-it";

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

    retrieveResourceData(unref(resource)!).then((data: string) => {
        textData.value = atob(data);
        parsedText.value = md.render(atob(data));
    });
});

const previewVisible = ref(false);
</script>

<template>
    <div @click="() => (!!textData ? (previewVisible = true) : '')">
        <MiniPreview :loading="!textData" hoverIcon="pi-search">
            <template #preview>
                <div v-if="!!textData" :innerText="textData" class="overflow-hidden !h-[calc(12rem-0.5rem)] whitespace-pre-wrap break-all p-2" />
            </template>
        </MiniPreview>

        <PreviewOverlay v-if="previewVisible" @close="previewVisible = false" :header="resource.filename">
            <article :innerHTML="parsedText" class="p-10 prose min-w-[100%] overflow-auto w-full bg-white"></article>
        </PreviewOverlay>
    </div>
</template>

<style scoped lang="scss"></style>
