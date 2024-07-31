<script setup lang="ts">
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

const audioData = ref("");

onMounted(() => {
    const { retrieveResourceData, resourceDataToTagValue } = useResourceTools(comp);

    retrieveResourceData(unref(resource)!).then((data: string) => {
        audioData.value = resourceDataToTagValue(unref(resource)!, data);
    });
});
</script>

<template>
    <div class="r-centered-grid content-center">
        <audio v-if="!!audioData" controls :src="audioData" />
        <Skeleton v-else title="Loading image..." class="!w-[calc(12rem-0.5rem)] !h-[calc(12rem-0.5rem)]"></Skeleton>
    </div>
</template>

<style scoped lang="scss"></style>
