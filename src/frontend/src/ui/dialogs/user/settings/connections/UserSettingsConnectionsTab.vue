<script setup lang="ts">
import BlockUI from "primevue/blockui";
import { type PropType, ref, toRefs, unref } from "vue";

import { ConnectorInstance, type ConnectorInstanceID } from "@common/data/entities/connector/ConnectorInstance";
import { UserSettings } from "@common/data/entities/user/UserSettings";

import { FrontendComponent } from "@/component/FrontendComponent";
import { EditUserSettingsAction } from "@/ui/actions/user/EditUserSettingsAction";

import ConnectorInstancesListbox from "@/ui/dialogs/user/settings/connections/ConnectorInstancesListbox.vue";
import NewConnectorInstance from "@/ui/dialogs/user/settings/connections/NewConnectorInstance.vue";

const comp = FrontendComponent.inject();
const props = defineProps({
    tabData: {
        type: Object as PropType<UserSettings>,
        required: true,
    },
});
const { tabData: userSettings } = toRefs(props);

const selectedConnectorInstance = ref<ConnectorInstanceID | undefined>();
const updatingSettings = ref(false);

function onCreateInstance(instance: ConnectorInstance): void {
    selectedConnectorInstance.value = instance.instance_id;

    // Immediately update the settings on the server to allow connecting the instance right away
    updatingSettings.value = true;

    const action = new EditUserSettingsAction(comp);
    action.prepare(unref(userSettings)!).done(() => (updatingSettings.value = false));
    action.execute();
}
</script>

<template>
    <BlockUI :blocked="updatingSettings">
        <div class="grid grid-rows-[auto_auto_1fr_auto] grid-cols-1 gap-1.5 w-full h-full">
            <div class="r-text-title">Connections</div>
            <div>
                To publish your project or export its data to an external service, you need to set up <em>connections</em> to these services. To add a new
                connection, use the drop-down list at the bottom of the connections list.
            </div>

            <ConnectorInstancesListbox v-model="selectedConnectorInstance" :user-settings="userSettings" />
            <NewConnectorInstance :user-settings="userSettings" @create-instance="onCreateInstance" />
        </div>
    </BlockUI>
</template>

<style scoped lang="scss"></style>
