<script setup lang="ts">
import Select from "primevue/select";
import { computed, nextTick, type PropType, ref, toRefs } from "vue";

import { Connector } from "@common/data/entities/connector/Connector";
import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { UserSettings } from "@common/data/entities/user/UserSettings";
import { scrollElementIntoView } from "@common/utils/HTMLUtils";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useConnectorInstancesTools } from "@/ui/tools/connector/ConnectorInstancesTools";

import ConnectorInstancesHeader from "@/ui/components/connector/ConnectorInstancesHeader.vue";

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
    // @ts-ignore
    return consStore.connectors.sort((con1: ConnectorInstance, con2: ConnectorInstance) => con1.name.toLowerCase().localeCompare(con2.name.toLowerCase()));
});
const { userSettings } = toRefs(props);
const { newInstance } = useConnectorInstancesTools(comp);

const selectedConnector = ref(null);

function onSelectConnector(connector: Connector): void {
    // Automatically deselect the newly selected item
    nextTick(() => {
        selectedConnector.value = null;
    });

    newInstance(userSettings!.value!.connector_instances, connector).then((newInst) => {
        scrollElementIntoView(`[id='connector-instance-${newInst.instance_id}']`, false);
        emits("create-instance", newInst);
    });
}
</script>

<template>
    <div class="flex flex-row content-center">
        <Select
            v-model="selectedConnector"
            :options="connectors"
            optionLabel="name"
            placeholder="Add a new connection..."
            class="w-full"
            variant="filled"
            @change="(event) => onSelectConnector(event.value as Connector)"
        >
            <template #option="connectorItem">
                <ConnectorInstancesHeader :connector-id="connectorItem.option.connector_id" />
            </template>
        </Select>
    </div>
</template>

<style scoped lang="scss"></style>
