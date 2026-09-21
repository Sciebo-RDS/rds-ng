<script setup lang="ts">
import { storeToRefs } from "pinia";
import { type PropType, toRefs, unref } from "vue";

import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance.ts";
import { findConnectorByInstanceID } from "@common/data/entities/connector/ConnectorInstanceUtils.ts";
import { isConnectorActivated } from "@common/data/entities/project/ProjectUtils.ts";
import { Project } from "@common/data/entities/project/Project";
import { UserSettings } from "@common/data/entities/user/UserSettings";

import { useConnectorsStore } from "@/data/stores/ConnectorsStore";

import ConnectorInstancesList from "@/ui/components/connector/ConnectorInstancesList.vue";
import UploadConnectionsListItem from "@/ui/dialogs/project/upload/UploadConnectionsListItem.vue";

const props = defineProps({
    project: {
        type: Object as PropType<Project>,
        required: true
    },
    userSettings: {
        type: Object as PropType<UserSettings>,
        required: true
    }
});
const { project, userSettings } = toRefs(props);

const consStore = useConnectorsStore();
const { connectors } = storeToRefs(consStore);

const connectorInstances: ConnectorInstance[] = [];
unref(userSettings)!.connector_instances.forEach((connectorInstance) => {
    const connector = findConnectorByInstanceID(unref(connectors)!, unref(userSettings)!.connector_instances, connectorInstance.instance_id);
    if (!!connector) {
        if (isConnectorActivated(unref(project), unref(userSettings), connector, unref(connectors))) {
            connectorInstances.push(connectorInstance);
        }
    }
});
</script>

<template>
    <ConnectorInstancesList :instances="connectorInstances" :connectors="connectors">
        <template #instance="slotProps">
            <UploadConnectionsListItem :project="project" :instance="slotProps.instance" />
        </template>
    </ConnectorInstancesList>
</template>

<style scoped lang="scss"></style>
