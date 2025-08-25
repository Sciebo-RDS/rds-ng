<script setup lang="ts">
import { storeToRefs } from "pinia";
import ScrollPanel from "primevue/scrollpanel";
import { nextTick, type PropType, ref, toRefs, unref } from "vue";

import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { connectorRequiresAuthorization, findConnectorByID, findConnectorInstanceByID } from "@common/data/entities/connector/ConnectorUtils.ts";
import { UserSettings } from "@common/data/entities/user/UserSettings";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore.ts";
import { useUserStore } from "@/data/stores/UserStore.ts";
import { useConnectorInstancesTools } from "@/ui/tools/connector/ConnectorInstancesTools.ts";
import { useUserTools } from "@/ui/tools/user/UserTools";

import ConnectionsList from "@/ui/dialogs/user/settings/connections/ConnectionsList.vue";
import NewConnection from "@/ui/dialogs/user/settings/connections/NewConnection.vue";

const comp = FrontendComponent.inject();
const props = defineProps({
    tabData: {
        type: Object as PropType<UserSettings>,
        required: true
    }
});
const { tabData: userSettings } = toRefs(props);

const consStore = useConnectorsStore();
const userStore = useUserStore();
const { userAuthorizations } = storeToRefs(userStore);

const { saveUserSettings } = useUserTools(comp);
const { requestInstanceAuthorization } = useConnectorInstancesTools(comp);

const newInstance = ref<ConnectorInstance | undefined>(undefined);

function onCreateInstance(instance: ConnectorInstance): void {
    saveUserSettings(unref(userSettings)!).then(() => {
        nextTick(() => {
            // Ensure that the instance has been added by the server
            if (!!findConnectorInstanceByID(unref(userSettings)!.connector_instances, instance.instance_id)) {
                const connector = findConnectorByID(consStore.connectors, instance.connector_id);
                if (!!connector && connectorRequiresAuthorization(connector)) {
                    newInstance.value = instance;
                    requestInstanceAuthorization(instance, consStore.connectors, unref(userAuthorizations));
                }
            }
        });
    });
}
</script>

<template>
    <div class="grid grid-rows-[auto_auto_1fr_auto] grid-cols-1 gap-1.5 w-full h-full">
        <div class="r-text-title">Connections</div>
        <div>
            To upload your project to an external service, you need to set up <em>connections</em> to these services. To add a new connection, use the drop-down
            list at the bottom of the connections list.
        </div>

        <ScrollPanel class="h-[29rem]">
            <ConnectionsList :user-settings="userSettings" :new-instance="newInstance" />
        </ScrollPanel>
        <NewConnection :user-settings="userSettings" @create-instance="onCreateInstance" />
    </div>
</template>

<style scoped lang="scss"></style>
