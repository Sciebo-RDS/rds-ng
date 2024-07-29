<script setup lang="ts">
import Button from "primevue/button";
import Portal from "primevue/portal";
import Skeleton from "primevue/skeleton";
import { onMounted, type PropType, ref, toRefs, unref } from "vue";

import { Resource } from "@common/data/entities/resource/Resource";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useResourceTools } from "@/ui/tools/resource/ResourceTools";

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
    <div class="r-centered-grid content-center max-w-inherit grid group flex place-items-center" @click="() => (!!textData ? (previewVisible = true) : '')">
        <div v-if="!!textData" class="group-hover:opacity-[25%] col-start-1 row-start-1 transition duration-200">
            <div v-if="!!textData" :innerText="textData" class="overflow-hidden !w-[calc(12rem-0.5rem)] !h-[calc(12rem-0.5rem)] truncate" />
        </div>
        <div v-if="!!textData" class="max-w-full col-start-1 row-start-1 hidden group-hover:inline">
            <i class="pi pi-search" style="color: black"></i>
        </div>

        <Skeleton v-else title="Loading image..." class="!w-[calc(12rem-0.5rem)] !h-[calc(12rem-0.5rem)]"></Skeleton>
        <Portal v-if="previewVisible">
            <div @click="previewVisible = false" class="z-50">
                <div class="fixed inset-0 bg-black bg-opacity-85 z-50"></div>

                <div class="fixed inset-0 flex justify-center items-center z-50 w-full flex-col">
                    <Button @click="previewVisible = false" class="absolute right-0 top-0" size="large" style="color: white" icon="pi pi-times" text></Button>
                    <div class="w-[80%] h-full bg-white flex flex-col divide-y-4 divide-slate-800/25" @click="(e) => e.stopPropagation()">
                        <div :innerText="resource.filename" class="text-xl text-center my-5 font-mono" />
                        <div v-if="!!parsedText" class="overflow-auto w-full">
                            <article :innerHTML="parsedText" class="p-10 prose min-w-[100%]"></article>
                        </div>
                    </div>
                </div>
            </div>
        </Portal>
    </div>
</template>

<style scoped lang="scss"></style>
