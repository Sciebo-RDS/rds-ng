<script setup lang="ts">
import { toRefs } from "vue";

import { UserSettings } from "@common/data/entities/user/UserSettings";

import ConnectorInstancesListbox from "@/ui/dialogs/usersettings/ConnectorInstancesListbox.vue";

const props = defineProps({
    tabData: {
        required: true
    }
});
const propRefs = toRefs(props);
const userSettings = propRefs.tabData!.value as UserSettings;
</script>

<template>
    <div class="grid grid-flow-row grid-cols-1 gap-1.5 w-full">
        <div class="r-text-title">Connections</div>
        <div>
            To publish your project or export its data to an external service, you need to set up <em>connections</em> to these services. To add a new connection,
            use the drop-down list at the bottom of the connections list.
        </div>
        <ConnectorInstancesListbox :user-settings="userSettings" />
    </div>
</template>

<style scoped lang="scss">

</style>
