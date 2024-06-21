<script setup lang="ts">
import { useUserStore } from "@/data/stores/UserStore";
import { storeToRefs } from "pinia";
import Listbox from "primevue/listbox";
import { computed, type PropType, toRefs, unref } from "vue";

import { ConnectorInstance, type ConnectorInstanceID } from "@common/data/entities/connector/ConnectorInstance";
import { groupConnectorInstances } from "@common/data/entities/connector/ConnectorInstanceUtils";
import { findConnectorByID, findConnectorInstanceByID } from "@common/data/entities/connector/ConnectorUtils";
import { UserSettings } from "@common/data/entities/user/UserSettings";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useConnectorInstancesTools } from "@/ui/tools/connector/ConnectorInstancesTools";

import ConnectorHeader from "@/ui/components/connector/ConnectorHeader.vue";
import ConnectorInstancesListboxItem from "@/ui/dialogs/user/settings/connections/ConnectorInstancesListboxItem.vue";

const comp = FrontendComponent.inject();
const consStore = useConnectorsStore();
const userStore = useUserStore();
const props = defineProps({
    userSettings: {
        type: Object as PropType<UserSettings>,
        required: true,
    },
});
const { connectors } = storeToRefs(consStore);
const { userAuthorizations } = storeToRefs(userStore);
const { userSettings } = toRefs(props);
const { editInstance, deleteInstance, requestInstanceAuthorization, revokeInstanceAuthorization } = useConnectorInstancesTools(comp);

const groupedInstances = computed(() => groupConnectorInstances(unref(userSettings)!.connector_instances, unref(connectors)));
const selectedInstance = defineModel<ConnectorInstanceID | undefined>();

function isInstanceSelected(instance: ConnectorInstance): boolean {
    return instance.instance_id === unref(selectedInstance);
}

function onEditInstance(instance: ConnectorInstance): void {
    editInstance(unref(userSettings)!.connector_instances, instance, findConnectorByID(unref(connectors), instance.connector_id));
}

function onDeleteKey() {
    if (unref(selectedInstance)) {
        const instance = findConnectorInstanceByID(unref(userSettings)!.connector_instances, unref(selectedInstance)!);
        if (instance) {
            deleteInstance(unref(userSettings)!.connector_instances, instance);
        }
    }
}
</script>

<template>
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
            itemGroup: 'coninst-listbox-item-group',
        }"
        @keydown="
            (event: KeyboardEvent) => {
                if (event.code == 'Delete') onDeleteKey();
            }
        "
    >
        <template #optiongroup="groupEntry">
            <ConnectorHeader :connector-id="groupEntry.option.connectorID" />
        </template>

        <template #option="instanceEntry">
            <ConnectorInstancesListboxItem
                :instance="instanceEntry.option"
                :is-selected="isInstanceSelected(instanceEntry.option)"
                @dblclick="onEditInstance(instanceEntry.option)"
                @authorize-instance="requestInstanceAuthorization(instanceEntry.option, connectors, userAuthorizations)"
                @unauthorize-instance="revokeInstanceAuthorization(instanceEntry.option)"
                @edit-instance="onEditInstance(instanceEntry.option)"
                @delete-instance="deleteInstance(userSettings!.connector_instances, instanceEntry.option)"
            />
        </template>

        <template #empty>
            <div class="r-text-caption-big r-small-caps grid justify-center">No connections</div>
        </template>
    </Listbox>
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
