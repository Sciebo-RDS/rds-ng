<script setup lang="ts">
import type { Project } from "@common/data/entities/project/Project";
import { storeToRefs } from "pinia";
import Listbox from "primevue/listbox";
import { computed, type PropType, toRefs, unref } from "vue";

import { groupConnectorInstances } from "@common/data/entities/connector/ConnectorUtils";
import { UserSettings } from "@common/data/entities/user/UserSettings";

import { useConnectorsStore } from "@/data/stores/ConnectorsStore";

import ConnectorHeader from "@/ui/components/connector/ConnectorHeader.vue";
import PublishConnectionsListboxItem from "@/ui/dialogs/project/publish/PublishConnectionsListboxItem.vue";

const consStore = useConnectorsStore();
const props = defineProps({
    project: {
        type: Object as PropType<Project>,
        required: true,
    },
    userSettings: {
        type: Object as PropType<UserSettings>,
        required: true,
    },
});
const { connectors } = storeToRefs(consStore);
const { project, userSettings } = toRefs(props);

const groupedInstances = computed(() => groupConnectorInstances(unref(userSettings)!.connector_instances, unref(connectors)!));
</script>

<template>
    <Listbox
        :options="groupedInstances"
        option-group-label="connectorID"
        option-group-children="connectorInstances"
        option-value="instance_id"
        class="w-full"
        :pt="{
            root: 'coninst-listbox',
            list: 'coninst-listbox-list',
            item: 'coninst-listbox-item',
            itemGroup: 'coninst-listbox-item-group',
        }"
    >
        <template #optiongroup="groupEntry">
            <ConnectorHeader :connector-id="groupEntry.option.connectorID" />
        </template>

        <template #option="instanceEntry">
            <PublishConnectionsListboxItem :project="project" :instance="instanceEntry.option" />
        </template>

        <template #empty>
            <div class="r-text-caption-big r-small-caps grid justify-center">No connections</div>
        </template>
    </Listbox>
</template>

<style scoped lang="scss">
:deep(.coninst-listbox) {
    @apply overflow-y-auto max-h-[27rem] #{!important};
}

:deep(.coninst-listbox-list) {
    @apply p-0 #{!important};
}

:deep(.coninst-listbox-item) {
    @apply border-solid border-b border-[--r-border-color] bg-inherit cursor-default #{!important};
}

:deep(.coninst-listbox-item-group) {
    @apply bg-[var(--r-shade-dark)] p-2 #{!important};
}
</style>
