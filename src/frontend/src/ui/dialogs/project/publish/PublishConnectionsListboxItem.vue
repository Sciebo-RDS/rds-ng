<script setup lang="ts">
import Button from "primevue/button";
import ProgressBar from "primevue/progressbar";
import { computed, type PropType, ref, toRefs, unref } from "vue";

import { ConnectorOptions } from "@common/data/entities/connector/Connector";
import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { findConnectorByID } from "@common/data/entities/connector/ConnectorUtils";
import { Project } from "@common/data/entities/project/Project";
import { ProjectStatistics } from "@common/data/entities/project/ProjectStatistics";
import { errorMessageDialog } from "@common/ui/dialogs/MessageDialog";
import { finishSentence, formatLocaleTimestamp } from "@common/utils/Strings";

import { FrontendComponent } from "@/component/FrontendComponent";
import { findConnectorCategory } from "@/data/entities/connector/ConnectorUtils";
import { getActiveProjectJob } from "@/data/entities/project/ProjectJobUtils";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { InitiateProjectJobAction } from "@/ui/actions/project/InitiateProjectJobAction";
import { ListProjectJobsAction } from "@/ui/actions/project/ListProjectJobsAction";

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
const category = unref(connector) ? findConnectorCategory(unref(connector)!) : undefined;

const activeJob = computed(() => getActiveProjectJob(unref(project)!, unref(instance)!));
const jobStats = computed(() => new ProjectStatistics(unref(project)!).getJobStatistics(unref(instance)!.instance_id));

const initiatePublish = ref(false);
const disablePublish = computed(() => {
    if (unref(connector)) {
        const publishOnce = (unref(connector)!.options & ConnectorOptions.PublishOnce) == ConnectorOptions.PublishOnce;
        return publishOnce && unref(jobStats).totalCount.succeeded >= 1;
    }
    return true;
});
const publishTitle = computed(() => (unref(initiatePublish) ? "Initiating..." : category?.verbAction));

function onPublish() {
    const conn = unref(connector);
    if (conn) {
        initiatePublish.value = true;

        const action = new InitiateProjectJobAction(comp);
        action
            .prepare(unref(project), conn, unref(instance))
            .done((_, success, msg) => {
                onPublishInitDone(success, msg);
            })
            .failed((_, msg) => {
                onPublishInitDone(false, msg);
            });
        action.execute();
    }
}

function onPublishInitDone(success: boolean, msg: string): void {
    // Only unlock the init-phase after updating the jobs list
    const listJobsAction = new ListProjectJobsAction(comp);
    listJobsAction.prepare().done(() => {
        initiatePublish.value = false;
    });
    listJobsAction.execute();

    if (!success) {
        errorMessageDialog(comp, `Unable to start ${category?.verbNoun.toLowerCase() || "job"}`, finishSentence(msg));
    }
}
</script>

<template>
    <div class="grid grid-rows-auto grid-flow-row gap-0 place-content-start group" :class="activeJob ? 'grid-cols-[1fr_33%]' : 'grid-cols-[1fr_min-content]'">
        <div :id="'connector-instance-' + instance!.instance_id" class="r-text-caption h-6 truncate" :title="instance!.name">{{ instance!.name }}</div>

        <div class="row-span-2 pl-1 content-center">
            <div v-if="activeJob" class="grid grid-flow-row text-sm">
                <span class="r-text-light italic justify-self-end truncate"
                    ><b>{{ category?.verbStatusProgressing }}:</b> {{ activeJob.message }}</span
                >
                <ProgressBar class="h-3" :value="Math.trunc(activeJob.progress * 100)" />
            </div>
            <div v-else>
                <Button
                    v-if="category"
                    :label="publishTitle"
                    :aria-label="publishTitle"
                    :title="disablePublish ? 'The project has already been ' + category.verbStatusDone.toLowerCase() : category.verbAction + ' the project'"
                    :loading="initiatePublish"
                    :disabled="disablePublish"
                    rounded
                    size="small"
                    icon="material-icons-outlined mi-rocket-launch"
                    loading-icon="material-icons-outlined mi-rocket-launch"
                    :pt="{ root: category.buttonClass }"
                    @click="onPublish"
                />
            </div>
        </div>

        <div class="truncate" :title="instance!.description">{{ instance!.description }}</div>

        <div class="grid grid-cols-[1fr_max-content] grid-flow-col pt-5 col-span-2 text-sm">
            <div v-if="category" class="grid grid-flow-col auto-cols-max gap-2 r-text-secondary italic">
                <b>Last {{ category.verbStatusDone }}: </b>
                <span class="pr-3">{{ jobStats.lastJob > 0 ? formatLocaleTimestamp(jobStats.lastJob) : "Never" }}</span>
                <b>Total {{ category.verbNounPlural }}:</b>
                <span>
                    {{ jobStats.totalCount.succeeded }}
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
