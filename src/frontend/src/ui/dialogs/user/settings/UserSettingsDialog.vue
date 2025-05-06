<script setup lang="ts">
import BlockUI from "primevue/blockui";
import { markRaw, ref } from "vue";

import VerticalTabs from "@common/ui/components/verticaltabview/VerticalTabs.vue";
import { useExtendedDialogTools } from "@common/ui/dialogs/ExtendedDialogTools";

import { UserSettings } from "@common/data/entities/user/UserSettings";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserTools } from "@/ui/tools/user/UserTools";

// import AppearanceTab from "@/ui/dialogs/user/settings/appearance/UserSettingsAppearanceTab.vue";
import ConnectionsTab from "@/ui/dialogs/user/settings/connections/UserSettingsConnectionsTab.vue";
import SupportTab from "@/ui/dialogs/user/settings/support/UserSettingsSupportTab.vue";

const comp = FrontendComponent.inject();

const { userSettingsUpdating } = useUserTools(comp);
const { dialogData } = useExtendedDialogTools();

const userSettings = ref<UserSettings>(dialogData.userData.userSettings);

const tabs = ref([
    { title: "Connections", component: markRaw(ConnectionsTab), icon: "mi-hub" },
    //{ title: "Appearance", component: markRaw(AppearanceTab), icon: "mi-brightness-medium" }, // TODO: add later
    { title: "About", component: markRaw(SupportTab), icon: "mi-feedback" }
]);
const tabIndices = {
    connections: 0,
    //appearance: 1, // TODO: add later
    support: 1 // 2
};
const activeTab = ref(tabIndices.connections);
</script>

<template>
    <BlockUI :blocked="userSettingsUpdating">
        <VerticalTabs v-model:active-tab="activeTab" :tabs="tabs" :tab-data="userSettings" />
    </BlockUI>
</template>

<style scoped lang="scss"></style>
