<script setup lang="ts">
import { markRaw, ref } from "vue";

import VerticalTabView from "@common/ui/components/VerticalTabView.vue";
import { extendedDialogTools } from "@common/ui/dialogs/ExtendedDialogTools";

import { UserSettings } from "@common/data/entities/user/UserSettings";

import { FrontendComponent } from "@/component/FrontendComponent";

import AppearanceTab from "@/ui/dialogs/user/UserSettingsAppearanceTab.vue";
import ConnectionsTab from "@/ui/dialogs/user/UserSettingsConnectionsTab.vue";
import SupportTab from "@/ui/dialogs/user/UserSettingsSupportTab.vue";

const { dialogData } = extendedDialogTools();

const comp = FrontendComponent.inject();
const userSettings = ref<UserSettings>(dialogData.userData.settings);

const tabs = ref([
    { title: "Connections", component: markRaw(ConnectionsTab), icon: "mi-hub" },
    { title: "Appearance", component: markRaw(AppearanceTab), icon: "mi-brightness-medium" },
    { title: "Help & Support", component: markRaw(SupportTab), icon: "mi-help-outline" }
]);
</script>

<template>
    <VerticalTabView :tabs="tabs" :tabData="userSettings" />
</template>

<style scoped lang="scss">

</style>
