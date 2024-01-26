<script setup lang="ts">
import { storeToRefs } from "pinia";
import { markRaw, ref, watch } from "vue";
import { array as yarray } from "yup";

import VerticalTabView from "@common/ui/components/VerticalTabView.vue";
import { useExtendedDialogTools } from "@common/ui/dialogs/ExtendedDialogTools";

import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { findConnectorByID } from "@common/data/entities/connector/ConnectorUtils";
import { UserSettings } from "@common/data/entities/user/UserSettings";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";

import AppearanceTab from "@/ui/dialogs/user/settings/appearance/UserSettingsAppearanceTab.vue";
import ConnectionsTab from "@/ui/dialogs/user/settings/connections/UserSettingsConnectionsTab.vue";
import SupportTab from "@/ui/dialogs/user/settings/support/UserSettingsSupportTab.vue";

const { dialogData, acceptDialog, useValidator } = useExtendedDialogTools();

const comp = FrontendComponent.inject();
const consStore = useConnectorsStore();
const { connectors } = storeToRefs(consStore);
const userSettings = ref<UserSettings>(dialogData.userData.userSettings);

const tabs = ref([
    { title: "Connections", component: markRaw(ConnectionsTab), icon: "mi-hub" },
    { title: "Appearance", component: markRaw(AppearanceTab), icon: "mi-brightness-medium" },
    { title: "Help & Support", component: markRaw(SupportTab), icon: "mi-help-outline" }
]);
const tabIndices = {
    connections: 0,
    appearance: 1,
    support: 2
};
const activeTab = ref(tabIndices.connections);

const validator = useValidator({
        connector_instances: yarray().required().test("all-connectors-exist", "The connector '${path}' doesn't exist", (value: ConnectorInstance[], ctx) => {
            for (const conInst of value) {
                if (!findConnectorByID(connectors.value, conInst.connector_id)) {
                    activeTab.value = tabIndices.connections;
                    return ctx.createError({ path: conInst.connector_id });
                }
            }
            return true;
        }).default(userSettings.value.connector_instances)
    }
);
watch(userSettings.value.connector_instances, (newConInsts) => {
    validator.setFieldValue("connector_instances", newConInsts);
});
</script>

<template>
    <form @submit.prevent="acceptDialog">
        <VerticalTabView v-model:active-tab="activeTab" :tabs="tabs" :tab-data="userSettings" />
    </form>
</template>

<style scoped lang="scss">

</style>
