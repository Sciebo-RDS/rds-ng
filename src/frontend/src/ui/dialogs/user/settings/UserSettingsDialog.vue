<script setup lang="ts">
import BlockUI from "primevue/blockui";
import { markRaw, ref } from "vue";

import VerticalTabs from "@common/ui/components/verticaltabview/VerticalTabs.vue";
import { useExtendedDialogTools } from "@common/ui/dialogs/ExtendedDialogTools";

import { UserSettings } from "@common/data/entities/user/UserSettings";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserTools } from "@/ui/tools/user/UserTools";

import ConnectionsTab from "@/ui/dialogs/user/settings/connections/UserSettingsConnectionsTab.vue";
import SupportTab from "@/ui/dialogs/user/settings/support/UserSettingsSupportTab.vue";
import AboutTab from "@/ui/dialogs/user/settings/about/UserSettingsAboutTab.vue";

const comp = FrontendComponent.inject();

const { userSettingsUpdating } = useUserTools(comp);
const { dialogData } = useExtendedDialogTools();

const userSettings = dialogData.userData.userSettings;

const tabs = ref([
    { title: "Connections", component: markRaw(ConnectionsTab), icon: "mi-add-link" },
    { title: "Help & Support", component: markRaw(SupportTab), icon: "mi-help-outline" },
    { title: "About", component: markRaw(AboutTab), icon: "mi-feedback" }
]);
const activeTab = dialogData.userData.activePage;
</script>

<template>
    <BlockUI :blocked="userSettingsUpdating" class="w-full">
        <VerticalTabs v-model:active-tab="activeTab" :tabs="tabs" :tab-data="userSettings" class="w-full" />
    </BlockUI>
</template>

<style scoped lang="scss"></style>
