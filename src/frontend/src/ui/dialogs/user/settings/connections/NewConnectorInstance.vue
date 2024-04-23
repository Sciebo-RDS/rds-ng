<script setup lang="ts">
import Dropdown from "primevue/dropdown";
import { computed, type PropType, toRefs } from "vue";

import { Connector } from "@common/data/entities/connector/Connector";
import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { UserSettings } from "@common/data/entities/user/UserSettings";
import { scrollElementIntoView } from "@common/utils/HTMLUtils";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useConnectorInstancesTools } from "@/ui/tools/connector/ConnectorInstancesTools";

import ConnectorHeader from "@/ui/components/connector/ConnectorHeader.vue";

const comp = FrontendComponent.inject();
const consStore = useConnectorsStore();
const props = defineProps({
    userSettings: {
        type: Object as PropType<UserSettings>,
        required: true,
    },
});
const emits = defineEmits<{
    (e: "create-instance", instance: ConnectorInstance): void;
}>();
const connectors = computed(() => {
    // @ts-ignore
    return consStore.connectors.sort((con1: ConnectorInstance, con2: ConnectorInstance) => con1.name.toLowerCase().localeCompare(con2.name.toLowerCase()));
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
                panel: 'r-z-index-toplevel',
            }"
        >
            <template #option="connectorItem">
                <ConnectorHeader :connector-id="connectorItem.option.connector_id" />
            </template>
        </Dropdown>
    </div>
</template>

<style scoped lang="scss"></style>
