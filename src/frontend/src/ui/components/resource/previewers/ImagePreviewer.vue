<script setup lang="ts">
import Image from "primevue/image";
import { type PropType, toRefs } from "vue";

import { Resource } from "@common/data/entities/resource/Resource";

import previewImage from "@assets/img/preview.png";

const props = defineProps({
    resource: {
        type: Object as PropType<Resource>,
        required: true,
    },
});
const { resource } = toRefs(props);
</script>

<template>
    <Image :src="previewImage" alt="Preview" :title="resource.filename" class="w-full h-full" preview />
</template>

<style scoped lang="scss"></style>
