<script setup lang="ts">
import Accordion from "primevue/accordion";
import AccordionContent from "primevue/accordioncontent";
import AccordionHeader from "primevue/accordionheader";
import Divider from "primevue/divider";
import AccordionPanel from "primevue/accordionpanel";
import { computed, type PropType, toRefs, unref } from "vue";

import { Connector } from "@common/data/entities/connector/Connector";
import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { groupConnectorInstances } from "@common/data/entities/connector/ConnectorInstanceUtils";

import ConnectorInstancesHeader from "@/ui/components/connector/ConnectorInstancesHeader.vue";

const props = defineProps({
    connectors: {
        type: Object as PropType<Connector[]>,
        required: true
    },
    instances: {
        type: Object as PropType<ConnectorInstance[]>,
        required: true
    }
});
const { connectors, instances } = toRefs(props);

const groupedInstances = computed(() => groupConnectorInstances(unref(instances), unref(connectors)));
</script>

<template>
    <Accordion :value="groupedInstances.map((inst) => inst.connectorID)" multiple :dt="{ 'content.padding': '0 1.125rem 1.125rem 0.75rem' }">
        <AccordionPanel v-for="group in groupedInstances" :key="group.connectorID" :value="group.connectorID" class="border-0">
            <AccordionHeader class="r-shade-dark rounded-xl mb-4">
                <ConnectorInstancesHeader :connector-id="group.connectorID" />
            </AccordionHeader>
            <AccordionContent>
                <div v-for="[index, instance] of group.connectorInstances.entries()" class="cursor-pointer">
                    <slot name="instance" :instance="instance" />
                    <Divider v-if="index < group.connectorInstances.length - 1" />
                </div>
            </AccordionContent>
        </AccordionPanel>
    </Accordion>
</template>

<style scoped lang="scss"></style>
