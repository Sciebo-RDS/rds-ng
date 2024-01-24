<script setup lang="ts">
import Dropdown from "primevue/dropdown";
import { computed, type PropType, toRefs } from "vue";

import { Connector } from "@common/data/entities/connector/Connector";
import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { UserSettings } from "@common/data/entities/user/UserSettings";
import { scrollElementIntoView } from "@common/utils/HTMLUtils";

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
const emits = defineEmits<{
    (e: "create-instance", instance: ConnectorInstance): void;
}>();
const connectors = computed(() => {
    return consStore.connectors.sort((con1, con2) => con1.name.toLowerCase().localeCompare(con2.name.toLowerCase()));
});
const { userSettings } = toRefs(props);
const { newInstance } = useConnectorInstancesTools(comp);

function onSelectConnector(connector: Connector): void {
    newInstance(userSettings!.value!.connector_instances, connector).then((newInst) => {
        scrollElementIntoView(`[id='connector-instance-${newInst.instance_id}']`, false);
        emits("create-instance", newInst);
    });
}
</script>

<template>
    <div>
        <Dropdown
            :options="connectors"
            optionLabel="name"
            placeholder="Add a new connection..."
            class="w-full"
            :autoOptionFocus="false"
            @change="(event) => onSelectConnector(event.value as Connector)"
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
