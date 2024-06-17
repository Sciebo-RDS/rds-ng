<script setup lang="ts">
import Tag from "primevue/tag";
import { type PropType, toRefs } from "vue";

import { ConnectorCategory } from "@/data/entities/connector/categories/ConnectorCategory";

const props = defineProps({
    category: {
        type: Object as PropType<ConnectorCategory>,
        required: true,
    },
});
const { category } = toRefs(props);
</script>

<template>
    <Tag
        :value="category!.name"
        :title="category!.description"
        :pt="{
            root: category!.tagClass,
        }"
    />
</template>

<style scoped lang="scss"></style>
