<script setup lang="ts">
import { computed, toRefs, unref } from "vue";

import { findConnectorByID } from "@common/data/entities/connector/ConnectorUtils";

import { useConnectorsStore } from "@/data/stores/ConnectorsStore";

const consStore = useConnectorsStore();
const props = defineProps({
    connectorId: {
        type: String,
        required: true
    }
});

const { connectorId } = toRefs(props);
const connector = computed(() => findConnectorByID(unref(consStore.connectors), connectorId!.value));
</script>

<template>
    <div v-if="connector" class="grid grid-rows-1 grid-cols-[min-content-1fr] grid-flow-col gap-3 place-content-start items-center">
        <img v-if="connector.logos.horizontal_logo" :src="connector.logos.horizontal_logo" class="h-4" alt="{{ connector.name }}" :title="connector.name" />
        <div class="truncate r-shade-text opacity-70" :title="connector.description">{{ connector.name }}</div>
    </div>
    <div v-else class="place-content-start items-center r-text-error">
        <div class="truncate opacity-70">Unknown connector <em>&lsquo;{{ connectorId }}&rsquo;</em></div>
    </div>
</template>

<style scoped lang="scss">

</style>
