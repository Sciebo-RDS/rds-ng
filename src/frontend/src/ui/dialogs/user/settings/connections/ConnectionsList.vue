<script setup lang="ts">
import { storeToRefs } from "pinia";
import Message from "primevue/message";
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
    }
});
const { userSettings } = toRefs(props);

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
                @authorize-instance="requestInstanceAuthorization(slotProps.instance, connectors, userAuthorizations)"
                @unauthorize-instance="revokeInstanceAuthorization(slotProps.instance)"
                @dblclick="onEditInstance(slotProps.instance)"
                @edit-instance="onEditInstance(slotProps.instance)"
                @delete-instance="onDeleteInstance(slotProps.instance)"
            />
        </template>
    </ConnectorInstancesList>
    <Message v-else severity="warn" :closable="false" class="m-0.5 mt-2">
        <div>
            You haven't added any connections to external services yet. To add a connection, select its desired type (i.e., the external service you want to
            upload your projects to) from the drop-down list below.
        </div>
    </Message>
</template>

<style scoped lang="scss"></style>
