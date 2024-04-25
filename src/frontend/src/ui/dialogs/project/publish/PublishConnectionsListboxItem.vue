<script setup lang="ts">
import Button from "primevue/button";
import { computed, type PropType, toRefs, unref } from "vue";

import { ConnectorOptions } from "@common/data/entities/connector/Connector";
import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { findConnectorByID } from "@common/data/entities/connector/ConnectorUtils";
import { Project } from "@common/data/entities/project/Project";
import { ProjectStatistics } from "@common/data/entities/project/ProjectStatistics";

import { FrontendComponent } from "@/component/FrontendComponent";
import { getConnectorCategory } from "@/data/entities/connector/ConnectorUtils";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { InitiateJobAction } from "@/ui/actions/project/InitiateJobAction";

const comp = FrontendComponent.inject();
const consStore = useConnectorsStore();
const props = defineProps({
    project: {
        type: Object as PropType<Project>,
        required: true,
    },
    instance: {
        type: Object as PropType<ConnectorInstance>,
        required: true,
    },
});

const { project, instance } = toRefs(props);
const connector = computed(() => findConnectorByID(consStore.connectors, unref(instance)!.connector_id));
const category = unref(connector) ? getConnectorCategory(unref(connector)!) : undefined;

const jobStats = new ProjectStatistics(unref(project)!).getJobStatistics(unref(instance)!.instance_id);
const disablePublish = computed(() => {
    if (unref(connector)) {
        const publishOnce = (unref(connector)!.options & ConnectorOptions.PublishOnce) == ConnectorOptions.PublishOnce;
        return publishOnce && jobStats.totalCount.done >= 1;
    }
    return true;
});

function onPublish() {
    if (!unref(project) || !unref(connector) || !unref(instance)) {
        return;
    }

    const action = new InitiateJobAction(comp);
    action.prepare(unref(project)!, unref(connector)!, unref(instance)!);
    action.execute();
}
</script>

<template>
    <div class="grid grid-rows-auto grid-cols-[1fr_min-content] grid-flow-row gap-0 place-content-start group">
        <div :id="'connector-instance-' + instance!.instance_id" class="r-text-caption h-6 truncate" :title="instance!.name">{{ instance!.name }}</div>

        <div class="row-span-2 pl-1 content-center">
            <Button
                v-if="category"
                :disabled="disablePublish"
                :title="disablePublish ? 'The project has already been ' + category.verbStatus.toLowerCase() : category.verbAction + ' the project'"
                rounded
                size="small"
                :aria-label="category.verbAction"
                :label="category.verbAction"
                icon="material-icons-outlined mi-rocket-launch"
                :pt="{ root: category.buttonClass }"
                @click="onPublish"
            />
        </div>

        <div class="truncate" :title="instance!.description">{{ instance!.description }}</div>

        <div class="grid grid-cols-[1fr_max-content] grid-flow-col pt-5 col-span-2 text-sm">
            <div v-if="category" class="grid grid-flow-col auto-cols-max gap-2 r-text-secondary italic">
                <b>Last {{ category.verbStatus }}: </b>
                <span class="pr-3">{{ jobStats.lastJob > 0 ? new Date(jobStats.lastJob * 1000).toLocaleString() : "Never" }}</span>
                <b>Total {{ category.verbNounPlural }}:</b>
                <span>
                    {{ jobStats.totalCount.done }}
                    <span v-if="jobStats.totalCount.failed > 0">(+ {{ jobStats.totalCount.failed }} failed)</span>
                </span>
            </div>
            <div v-else class="italic r-text-error">Unknown connector category</div>
            <img
                v-if="connector && connector.logos.horizontal_logo"
                :src="connector.logos.horizontal_logo"
                class="h-4 opacity-50"
                alt="{{ connector.name }}"
                :title="connector.name"
            />
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
