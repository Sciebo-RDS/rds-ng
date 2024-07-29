<script setup lang="ts">
import Button from "primevue/button";
import Portal from "primevue/portal";
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
    <div class="r-centered-grid content-center max-w-inherit grid group flex place-items-center" @click="() => (!!pdfData ? (previewVisible = true) : '')">
        <div v-if="!!pdfData" class="group-hover:brightness-[35%] group-hover:grayscale col-start-1 row-start-1 transition duration-200">
            <object :data="pdfData" :type="resource.mime_type" style="pointer-events: none" class="h-[calc(12rem-0.5rem)]"></object>
        </div>
        <div v-if="!!pdfData" class="max-w-full col-start-1 row-start-1 hidden group-hover:inline">
            <i class="pi pi-search brightness-100" style="color: white"></i>
        </div>
        <Skeleton v-else title="Loading PDF..." class="!w-[calc(12rem-0.5rem)] !h-[calc(12rem-0.5rem)] col-start-1 row-start-1"></Skeleton>

        <Portal v-if="previewVisible">
            <div @click="previewVisible = false" class="z-50">
                <div class="fixed inset-0 bg-black bg-opacity-85 z-49"></div>

                <div class="fixed inset-0 flex justify-center items-center z-50 w-full flex flex-col">
                    <Button @click="previewVisible = false" class="absolute right-0 top-0" size="large" style="color: white" icon="pi pi-times" text></Button>

                    <object :data="pdfData" :type="resource.mime_type" class="w-[80%] h-full"></object>
                </div>
            </div>
        </Portal>
    </div>
</template>

<style scoped lang="scss"></style>
