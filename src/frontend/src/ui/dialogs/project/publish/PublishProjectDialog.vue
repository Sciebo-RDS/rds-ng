<script setup lang="ts">
import { storeToRefs } from "pinia";
import Button from "primevue/button";
import { computed } from "vue";

import { groupConnectorInstances } from "@common/data/entities/connector/ConnectorUtils";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useUserStore } from "@/data/stores/UserStore";
import ConnectorHeader from "@/ui/components/connector/ConnectorHeader.vue";

const comp = FrontendComponent.inject();
const consStore = useConnectorsStore();
const userStore = useUserStore();
const { connectors } = storeToRefs(consStore);
const { userSettings } = storeToRefs(userStore);

const groupedInstances = computed(() => groupConnectorInstances(userSettings.value.connector_instances, connectors.value));
</script>

<template>
    <div class="grid grid-rows-auto grid-flow-row grid-cols-[1fr] gap-1.5 w-full h-full">
        <div>
            To publish / export a project to a service, click on the service's corresponding <em>Publish</em> / <em>Export</em> button.
        </div>
        <div class="font-bold italic mb-2">
            This dialog is only a placeholder without functionality! It is solely here to show the basic workflow of publishing a project.
        </div>

        <div v-for="group in groupedInstances" class="p-listbox">
            <ConnectorHeader :connector-id="group.connectorID" class="r-shade-dark p-2 rounded p-listbox-item-group" />

            <div class="divide-y">
                <div v-for="instance in group.connectorInstances" class="grid grid-cols-[1fr_min-content] gap-2 p-2">
                    <div class="mr-auto mb-1">
                        <div class="r-text-caption h-6 truncate" :title="instance.name">{{ instance.name }}</div>
                        <div class="" :title="instance.description">{{ instance.description }}</div>
                    </div>
                    <div class="pt-1">
                        <Button label="Publish" size="small" rounded disabled />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">

</style>
