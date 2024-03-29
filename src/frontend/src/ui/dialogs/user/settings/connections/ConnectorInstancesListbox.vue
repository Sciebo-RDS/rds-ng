<script setup lang="ts">
import { storeToRefs } from "pinia";
import Listbox from "primevue/listbox";
import { computed, type PropType, toRefs } from "vue";

import { ConnectorInstance, type ConnectorInstanceID } from "@common/data/entities/connector/ConnectorInstance";
import { findConnectorByID, findConnectorInstanceByID, groupConnectorInstances } from "@common/data/entities/connector/ConnectorUtils";
import { UserSettings } from "@common/data/entities/user/UserSettings";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useConnectorInstancesTools } from "@/ui/tools/ConnectorInstancesTools";

import ConnectorHeader from "@/ui/components/connector/ConnectorHeader.vue";
import ConnectorInstancesListboxItem from "@/ui/dialogs/user/settings/connections/ConnectorInstancesListboxItem.vue";

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
const { editInstance, deleteInstance } = useConnectorInstancesTools(comp);

const groupedInstances = computed(() => groupConnectorInstances(userSettings!.value!.connector_instances, connectors.value));
const selectedInstance = defineModel<ConnectorInstanceID | undefined>();

function isInstanceSelected(instance: ConnectorInstance): boolean {
    return instance.instance_id === selectedInstance.value;
}

function onEditInstance(instance: ConnectorInstance): void {
    editInstance(userSettings!.value!.connector_instances, instance, findConnectorByID(connectors.value, instance.connector_id));
}

function onDeleteKey() {
    if (selectedInstance.value) {
        const instance = findConnectorInstanceByID(userSettings!.value!.connector_instances, selectedInstance.value);
        if (instance) {
            deleteInstance(userSettings!.value!.connector_instances, instance);
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
                <ConnectorHeader :connector-id="groupEntry.option.connectorID" />
            </template>

            <template #option="instanceEntry">
                <ConnectorInstancesListboxItem
                    :instance="instanceEntry.option"
                    :is-selected="isInstanceSelected(instanceEntry.option)"
                    @dblclick="onEditInstance(instanceEntry.option)"
                    @edit-instance="onEditInstance(instanceEntry.option)"
                    @delete-instance="deleteInstance(userSettings!.connector_instances, instanceEntry.option)"
                />
            </template>

            <template #empty>
                <div class="r-text-caption-big r-small-caps grid justify-center">No connections</div>
            </template>
        </Listbox>
    </div>
</template>

<style scoped lang="scss">
:deep(.coninst-listbox) {
    @apply overflow-y-auto max-h-[27rem] #{!important};
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
