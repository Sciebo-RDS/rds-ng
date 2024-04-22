<script setup lang="ts">
import Button from "primevue/button";
import { computed, type PropType, toRefs, unref } from "vue";

import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { findConnectorByID } from "@common/data/entities/connector/ConnectorUtils";

import { getConnectorCategory } from "@/data/entities/connector/ConnectorUtils";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";

const consStore = useConnectorsStore();
const props = defineProps({
    instance: {
        type: Object as PropType<ConnectorInstance>,
        required: true,
    },
});

const { instance } = toRefs(props);
const connector = computed(() => findConnectorByID(consStore.connectors, instance.value.connector_id));
const category = unref(connector) ? getConnectorCategory(unref(connector)!) : undefined;
</script>

<template>
    <div class="grid grid-rows-auto grid-cols-[1fr_min-content] grid-flow-row gap-0 place-content-start group">
        <div :id="'connector-instance-' + instance!.instance_id" class="r-text-caption h-6 truncate" :title="instance!.name">{{ instance!.name }}</div>

        <div class="row-span-2 pl-1 content-center">
            <Button
                v-if="category"
                rounded
                size="small"
                :aria-label="category.verbAction"
                :label="category.verbAction"
                icon="material-icons-outlined mi-rocket-launch"
                :pt="{ root: category.buttonClass }"
            />
        </div>

        <div class="truncate" :title="instance!.description">{{ instance!.description }}</div>

        <div class="grid grid-cols-[1fr_max-content] grid-flow-col pt-5 col-span-2">
            <span>
                <b>Status: </b>
                <span class="italic">
                    <span v-if="connector">We don't have that yet...</span>
                    <span v-else class="r-text-error">Connector not found</span>
                </span>
            </span>
            <img
                v-if="connector && connector.logos.horizontal_logo"
                :src="connector.logos.horizontal_logo"
                class="h-4 opacity-50"
                alt="{{ connector.name }}"
                :title="connector.name"
            />
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
