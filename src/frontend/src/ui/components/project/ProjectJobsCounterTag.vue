<script setup lang="ts">
import Tag from "primevue/tag";
import { type PropType, toRefs } from "vue";

import { ConnectorCategory } from "@/data/entities/connector/categories/ConnectorCategory";

const props = defineProps({
    category: {
        type: Object as PropType<ConnectorCategory>,
        required: true,
    },
    value: {
        type: Number,
        required: true,
    },
    instanceNames: {
        type: Object as PropType<String[]>,
        default: [],
    },
});
const { category, value, instanceNames } = toRefs(props);
</script>

<template>
    <Tag
        :title="category.verbStatusDone + ' to: ' + instanceNames.join(', ')"
        :pt="{
            root: category!.tagClass,
        }"
    >
        <span>{{ category.verbNounPlural }}:&nbsp;</span><span class="font-normal">{{ value }}</span>
    </Tag>
</template>

<style scoped lang="scss"></style>
