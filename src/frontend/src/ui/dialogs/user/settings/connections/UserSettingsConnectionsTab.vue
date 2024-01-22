<script setup lang="ts">
import { type PropType, toRefs } from "vue";

import { UserSettings } from "@common/data/entities/user/UserSettings";

import ConnectorInstancesListbox from "@/ui/dialogs/user/settings/connections/ConnectorInstancesListbox.vue";
import NewConnectorInstance from "@/ui/dialogs/user/settings/connections/NewConnectorInstance.vue";

const props = defineProps({
    tabData: {
        type: Object as PropType<UserSettings>,
        required: true
    }
});
const propRefs = toRefs(props);
const userSettings = propRefs.tabData!;
</script>

<template>
    <div class="grid grid-rows-[auto_auto_1fr_auto] grid-cols-1 gap-1.5 w-full h-full">
        <div class="r-text-title">Connections</div>
        <div>
            To publish your project or export its data to an external service, you need to set up <em>connections</em> to these services. To add a new connection,
            use the drop-down list at the bottom of the connections list.
        </div>

        <ConnectorInstancesListbox :user-settings="userSettings" />
        <NewConnectorInstance :user-settings="userSettings" />
    </div>
</template>

<style scoped lang="scss">

</style>
