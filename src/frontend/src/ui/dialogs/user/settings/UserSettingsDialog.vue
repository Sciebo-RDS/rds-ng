<script setup lang="ts">
import { markRaw, ref } from "vue";

import VerticalTabView from "@common/ui/components/VerticalTabView.vue";
import { useExtendedDialogTools } from "@common/ui/dialogs/ExtendedDialogTools";

import { UserSettings } from "@common/data/entities/user/UserSettings";

import { FrontendComponent } from "@/component/FrontendComponent";

import AppearanceTab from "@/ui/dialogs/user/settings/appearance/UserSettingsAppearanceTab.vue";
import ConnectionsTab from "@/ui/dialogs/user/settings/connections/UserSettingsConnectionsTab.vue";
import SupportTab from "@/ui/dialogs/user/settings/support/UserSettingsSupportTab.vue";

const { dialogData } = useExtendedDialogTools();

const comp = FrontendComponent.inject();
const userSettings = ref<UserSettings>(dialogData.userData.userSettings);

const tabs = ref([
    { title: "Connections", component: markRaw(ConnectionsTab), icon: "mi-hub" },
    { title: "Appearance", component: markRaw(AppearanceTab), icon: "mi-brightness-medium" },
    { title: "Help & Support", component: markRaw(SupportTab), icon: "mi-help-outline" }
]);
</script>

<template>
    <VerticalTabView :tabs="tabs" :tab-data="userSettings" />
</template>

<style scoped lang="scss">

</style>
