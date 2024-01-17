<script setup lang="ts">
import { toRefs } from "vue";

import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";

const props = defineProps({
    instance: {
        type: ConnectorInstance,
        required: true
    },
    isSelected: {
        type: Boolean,
        default: false
    }
});

const { instance } = toRefs(props);
</script>

<template>
    <div class="grid grid-rows-[auto_auto] grid-cols-[1fr_min-content] grid-flow-row gap-0 place-content-start group">
        <div class="r-text-caption h-6 truncate" :title="instance!.name">{{ instance!.name }}</div>
    </div>
</template>

<style scoped lang="scss">

</style>
