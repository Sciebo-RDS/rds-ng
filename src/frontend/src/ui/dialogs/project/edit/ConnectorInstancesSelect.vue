<script setup lang="ts">
import { FrontendComponent } from "@/component/FrontendComponent";
import { storeToRefs } from "pinia";
import "primeicons/primeicons.css";
import Button from "primevue/button";
import Checkbox from "primevue/checkbox";
import ScrollPanel from "primevue/scrollpanel";
import { computed, toRefs } from "vue";

import { groupConnectorInstances } from "@common/data/entities/connector/ConnectorInstanceUtils";

const comp = FrontendComponent.inject();

import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useUserStore } from "@/data/stores/UserStore";
import { useUserTools } from "@/ui/tools/user/UserTools";

const { editUserSettings } = useUserTools(comp);

import ConnectorInstancesHeader from "@/ui/components/connector/ConnectorInstancesHeader.vue";

const consStore = useConnectorsStore();
const userStore = useUserStore();
const props = defineProps({
    disabled: {
        type: Boolean,
        default: false
    }
});
const { connectors } = storeToRefs(consStore);
const { userSettings } = storeToRefs(userStore);
const { disabled } = toRefs(props);

const groupedInstances = computed(() => groupConnectorInstances(userSettings.value.connector_instances, connectors.value));
const model = defineModel({ default: [] });
</script>

<template>
    <ScrollPanel>
        <div v-for="group of groupedInstances" :class="{ 'p-disabled': disabled }">
            <ConnectorInstancesHeader :connector-id="group.connectorID" class="r-shade-dark rounded list-entry !h-10" />

            <div v-for="instance of group.connectorInstances" :key="instance.instance_id" class="flex align-items-center list-entry !py-1">
                <Checkbox v-model="model" :inputId="instance.instance_id" :value="instance.instance_id" :disabled="disabled" size="large" class="self-center" />
                <label :for="instance.instance_id" class="pl-1.5">{{ instance.name }}</label>
            </div>
        </div>
        <div v-if="groupedInstances.length === 0" class="justify-items-center content-center h-full space-y-3">
            <i class="pi pi-exclamation-circle" style="font-size: 2.5rem"></i>
            <div class="justify-items-center">
                <div class="font-bold">No connections</div>
                <div class="text-sm">
                    Set them up in your
                    <Button @click="editUserSettings(userSettings)" label="settings" class="p-0" text />
                    !
                </div>
            </div>
        </div>
    </ScrollPanel>
</template>

<style scoped lang="scss">
.list-entry {
    @apply p-0.5 pl-2;
}
</style>
