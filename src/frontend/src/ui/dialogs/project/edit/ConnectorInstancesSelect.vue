<script setup lang="ts">
import { storeToRefs } from "pinia";
import Checkbox from "primevue/checkbox";
import ScrollPanel from "primevue/scrollpanel";
import { computed, toRefs } from "vue";

import { groupConnectorInstances } from "@common/data/entities/connector/ConnectorInstanceUtils";

import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useUserStore } from "@/data/stores/UserStore";

import ConnectorHeader from "@/ui/components/connector/ConnectorHeader.vue";

const consStore = useConnectorsStore();
const userStore = useUserStore();
const props = defineProps({
    disabled: {
        type: Boolean,
        default: false,
    },
});
const { connectors } = storeToRefs(consStore);
const { userSettings } = storeToRefs(userStore);
const { disabled } = toRefs(props);

const groupedInstances = computed(() => groupConnectorInstances(userSettings.value.connector_instances, connectors.value));
const model = defineModel({ default: [] });
</script>

<template>
    <ScrollPanel>
        <div v-for="group of groupedInstances" :class="{ 'p-disabled': disabled }">
            <ConnectorHeader :connector-id="group.connectorID" class="r-shade-dark rounded list-entry" />

            <div v-for="instance of group.connectorInstances" :key="instance.instance_id" class="flex align-items-center list-entry">
                <Checkbox v-model="model" :inputId="instance.instance_id" :value="instance.instance_id" :disabled="disabled" class="self-center" />
                <label :for="instance.instance_id" class="pl-1.5">{{ instance.name }}</label>
            </div>
        </div>
    </ScrollPanel>
</template>

<style scoped lang="scss">
.list-entry {
    @apply p-0.5 pl-2;
}
</style>
