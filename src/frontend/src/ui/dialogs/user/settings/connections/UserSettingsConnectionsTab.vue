<script setup lang="ts">
import ScrollPanel from "primevue/scrollpanel";
import { type PropType, toRefs, unref } from "vue";

import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { UserSettings } from "@common/data/entities/user/UserSettings";

import { FrontendComponent } from "@/component/FrontendComponent";
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

const { saveUserSettings } = useUserTools(comp);

function onCreateInstance(instance: ConnectorInstance): void {
    saveUserSettings(unref(userSettings)!);
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
            <ConnectionsList :user-settings="userSettings" />
        </ScrollPanel>
        <NewConnection :user-settings="userSettings" @create-instance="onCreateInstance" />
    </div>
</template>

<style scoped lang="scss"></style>
