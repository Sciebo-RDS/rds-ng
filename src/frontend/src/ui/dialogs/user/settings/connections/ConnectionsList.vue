<script setup lang="ts">
import { storeToRefs } from "pinia";
import Card from "primevue/card";
import { type PropType, toRefs, unref } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useUserStore } from "@/data/stores/UserStore";
import { useConnectorInstancesTools } from "@/ui/tools/connector/ConnectorInstancesTools";
import { useUserTools } from "@/ui/tools/user/UserTools";

import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { findConnectorByID } from "@common/data/entities/connector/ConnectorUtils";
import { UserSettings } from "@common/data/entities/user/UserSettings";

import ConnectorInstancesList from "@/ui/components/connector/ConnectorInstancesList.vue";
import ConnectionsListItem from "@/ui/dialogs/user/settings/connections/ConnectionsListItem.vue";

const comp = FrontendComponent.inject();
const props = defineProps({
    userSettings: {
        type: Object as PropType<UserSettings>,
        required: true
    },
    newInstance: {
        type: Object as PropType<ConnectorInstance>,
        default: undefined
    }
});
const { userSettings, newInstance } = toRefs(props);

const consStore = useConnectorsStore();
const userStore = useUserStore();
const { connectors } = storeToRefs(consStore);
const { userAuthorizations } = storeToRefs(userStore);

const { editInstance, deleteInstance, requestInstanceAuthorization, revokeInstanceAuthorization } = useConnectorInstancesTools(comp);
const { saveUserSettings } = useUserTools(comp);

function onEditInstance(instance: ConnectorInstance): void {
    editInstance(unref(userSettings)!.connector_instances, instance, findConnectorByID(unref(connectors), instance.connector_id)).then(() => {
        saveUserSettings(unref(userSettings)!);
    });
}

function onDeleteInstance(instance: ConnectorInstance) {
    deleteInstance(unref(userSettings)!.connector_instances, instance);
    saveUserSettings(unref(userSettings)!);
}
</script>

<template>
    <ConnectorInstancesList v-if="userSettings.connector_instances.length > 0" :instances="userSettings.connector_instances" :connectors="connectors">
        <template #instance="slotProps">
            <ConnectionsListItem
                :instance="slotProps.instance"
                :is-new="!!newInstance && slotProps.instance.instance_id == newInstance.instance_id"
                @authorize-instance="requestInstanceAuthorization(slotProps.instance, connectors, userAuthorizations)"
                @unauthorize-instance="revokeInstanceAuthorization(slotProps.instance)"
                @dblclick="onEditInstance(slotProps.instance)"
                @edit-instance="onEditInstance(slotProps.instance)"
                @delete-instance="onDeleteInstance(slotProps.instance)"
            />
        </template>
    </ConnectorInstancesList>
    <Card v-else class="bg-amber-100 text-amber-700 !p-0 mt-4 w-full" :pt="{ title: '!text-base', caption: 'h-5', body: 'p-3 px-5' }">
        <template #title>
            <div class="flex items-center gap-1">
                <span class="material-icons-outlined mi-link-off !text-xl" />
                <span class="">No connections added</span>
            </div>
        </template>
        <template #content>
            <span class="text-sm">
                You haven't added any connections to external services yet. To add a connection, select its desired type (i.e., the external service you want to
                upload your projects to) from the drop-down list below.
            </span>
        </template>
    </Card>
</template>

<style scoped lang="scss"></style>
