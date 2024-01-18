<script setup lang="ts">
import Listbox from "primevue/listbox";
import { ref, toRefs } from "vue";

import { ConnectorInstance, type ConnectorInstanceID } from "@common/data/entities/connector/ConnectorInstance";
import { groupConnectorInstances } from "@common/data/entities/connector/ConnectorUtils";
import { UserSettings } from "@common/data/entities/user/UserSettings";

import ConnectorInstancesListboxGroup from "@/ui/dialogs/usersettings/ConnectorInstancesListboxGroup.vue";
import ConnectorInstancesListboxItem from "@/ui/dialogs/usersettings/ConnectorInstancesListboxItem.vue";

const props = defineProps({
    userSettings: {
        type: UserSettings,
        required: true
    }
});
const { userSettings } = toRefs(props);

const groupedInstances = ref(groupConnectorInstances(userSettings!.value!.connector_instances));
const selectedInstance = ref<ConnectorInstanceID | undefined>();

function isInstanceSelected(instance: ConnectorInstance): boolean {
    return instance.instance_id === selectedInstance.value;
}
</script>

<template>
    <div>
        <Listbox
            v-model="selectedInstance"
            :options="groupedInstances"
            option-group-label="connectorID"
            option-group-children="connectorInstances"
            option-value="instance_id"
            class="w-full"
            :pt="{
                list: 'coninst-listbox-list',
                itemGroup: 'coninst-listbox-item-group'
            }"
        >
            <template #optiongroup="groupEntry">
                <ConnectorInstancesListboxGroup
                    :group="groupEntry.option"
                />
            </template>
            <template #option="instanceEntry">
                <ConnectorInstancesListboxItem
                    :instance="instanceEntry.option"
                    :is-selected="isInstanceSelected(instanceEntry.option)"
                />
            </template>
            <template #empty>
                <div class="r-text-caption-big r-small-caps grid justify-center">No connections</div>
            </template>
        </Listbox>
    </div>
</template>

<style scoped lang="scss">
:deep(.coninst-listbox-list) {
    @apply p-0 #{!important};
}

:deep(.coninst-listbox-item-group) {
    @apply bg-[var(--r-shade-dark)] p-2 #{!important};
}
</style>
