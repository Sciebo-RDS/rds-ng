<script setup lang="ts">
import { storeToRefs } from "pinia";
import Dropdown from "primevue/dropdown";
import { type PropType, toRefs } from "vue";

import { Connector } from "@common/data/entities/connector/Connector";
import { UserSettings } from "@common/data/entities/user/UserSettings";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useConnectorInstancesTools } from "@/ui/tools/ConnectorInstancesTools";

const comp = FrontendComponent.inject();
const consStore = useConnectorsStore();
const props = defineProps({
    userSettings: {
        type: Object as PropType<UserSettings>,
        required: true
    }
});
const { connectors } = storeToRefs(consStore);
const { userSettings } = toRefs(props);
const { createInstance } = useConnectorInstancesTools(comp);
</script>

<template>
    <div>
        <Dropdown
            :options="connectors"
            optionLabel="name"
            placeholder="Add a new connection..."
            class="w-full"
            :autoOptionFocus="false"
            @change="(event) => createInstance(userSettings!.connector_instances, event.value as Connector)"
            :pt="{
                panel: 'r-z-index-toplevel'
            }"
        >
            <template #option="connectorItem">
                <div class="grid grid-rows-1 grid-cols-[min-content-1fr] grid-flow-col gap-3 place-content-start items-center">
                    <img v-if="connectorItem.option.logos.horizontal_logo" :src="connectorItem.option.logos.horizontal_logo" class="h-4" alt="{{ connectorItem.option.name }}" :title="connectorItem.option.description" />
                    <div :title="connectorItem.option.description">{{ connectorItem.option.name }}</div>
                </div>
            </template>
        </Dropdown>
    </div>
</template>

<style scoped lang="scss">

</style>
