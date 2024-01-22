<script setup lang="ts">
import { storeToRefs } from "pinia";
import Dropdown from "primevue/dropdown";
import Listbox from "primevue/listbox";
import { computed, type PropType, ref, toRefs, unref } from "vue";

import { Connector } from "@common/data/entities/connector/Connector";
import { ConnectorInstance, type ConnectorInstanceID } from "@common/data/entities/connector/ConnectorInstance";
import { findConnectorInstanceByID, groupConnectorInstances } from "@common/data/entities/connector/ConnectorUtils";
import { UserSettings } from "@common/data/entities/user/UserSettings";

import { useConnectorsStore } from "@/data/stores/ConnectorsStore";

import ConnectorInstancesListboxGroup from "@/ui/dialogs/user/settings/connections/ConnectorInstancesListboxGroup.vue";
import ConnectorInstancesListboxItem from "@/ui/dialogs/user/settings/connections/ConnectorInstancesListboxItem.vue";

const consStore = useConnectorsStore();
const props = defineProps({
    userSettings: {
        type: Object as PropType<UserSettings>,
        required: true
    }
});
const { connectors } = storeToRefs(consStore);
const { userSettings } = toRefs(props);

const groupedInstances = computed(() => groupConnectorInstances(userSettings!.value!.connector_instances, unref(connectors.value)));
const selectedInstance = ref<ConnectorInstanceID | undefined>();

function isInstanceSelected(instance: ConnectorInstance): boolean {
    return instance.instance_id === selectedInstance.value;
}

function addInstance(connector: Connector): void {
    // TODO
    const instances = userSettings!.value.connector_instances;
    const instanceID = instances.length ? instances[instances.length - 1].instance_id + 1 : 1;
    instances.push(
        new ConnectorInstance(instanceID, connector.connector_id, "I am new!", "And not unique...")
    );

    selectedInstance.value = instanceID;
}

function editInstance(instance: ConnectorInstance): void {
    // TODO
}

function deleteInstance(instance: ConnectorInstance): void {
    const index = userSettings!.value.connector_instances.indexOf(instance);
    if (index != -1) {
        userSettings!.value.connector_instances.splice(index, 1);
    }
}

function onDeleteKey() {
    if (selectedInstance.value) {
        const instance = findConnectorInstanceByID(userSettings!.value!.connector_instances, selectedInstance.value);
        if (instance) {
            deleteInstance(instance);
        }
    }
}
</script>

<template>
    <div>
        <Listbox
            v-model="selectedInstance"
            :options="groupedInstances"
            option-group-label="connectorID"
            option-group-children="connectorInstances"
            option-value="instance_id"
            class="w-full"
            :pt="{
                root: 'coninst-listbox',
                list: 'coninst-listbox-list',
                item: 'coninst-listbox-item',
                itemGroup: 'coninst-listbox-item-group'
            }"
            @keydown="(event: KeyboardEvent) => { if (event.code == 'Delete') onDeleteKey(); }"
        >
            <template #optiongroup="groupEntry">
                <ConnectorInstancesListboxGroup
                    :group="groupEntry.option"
                />
            </template>
            <template #option="instanceEntry">
                <ConnectorInstancesListboxItem
                    :instance="instanceEntry.option"
                    :is-selected="isInstanceSelected(instanceEntry.option)"
                    @edit-instance="editInstance"
                    @delete-instance="deleteInstance"
                />
            </template>
            <template #empty>
                <div class="r-text-caption-big r-small-caps grid justify-center">No connections</div>
            </template>
        </Listbox>

        <Dropdown
            :options="connectors"
            optionLabel="name"
            placeholder="Add a new connection..."
            class="w-full mt-1"
            :autoOptionFocus="false"
            @change="(event) => addInstance(event.value as Connector)"
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
:deep(.coninst-listbox) {
    @apply overflow-y-auto max-h-[calc(100vh-40rem)] #{!important};
}

:deep(.coninst-listbox-list) {
    @apply p-0 #{!important};
}

:deep(.coninst-listbox-item) {
    @apply border-solid border-b border-[--r-border-color] #{!important};
}

:deep(.coninst-listbox-item-group) {
    @apply bg-[var(--r-shade-dark)] p-2 #{!important};
}
</style>
