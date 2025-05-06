<script setup lang="ts">
import { storeToRefs } from "pinia";
import { type PropType, toRefs } from "vue";

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
</script>

<template>
    <ConnectorInstancesList :instances="userSettings.connector_instances" :connectors="connectors">
        <template #instance="slotProps">
            <UploadConnectionsListItem :project="project" :instance="slotProps.instance" />
        </template>
    </ConnectorInstancesList>
</template>

<style scoped lang="scss"></style>
