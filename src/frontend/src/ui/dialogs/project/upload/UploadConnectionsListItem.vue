<script setup lang="ts">
import { storeToRefs } from "pinia";
import Button from "primevue/button";
import ProgressBar from "primevue/progressbar";
import Tag from "primevue/tag";
import { computed, type PropType, ref, toRefs, unref } from "vue";

import { ConnectorOptions } from "@common/data/entities/connector/Connector";
import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { connectorInstanceIsAuthorized } from "@common/data/entities/connector/ConnectorInstanceUtils";
import { connectorRequiresAuthorization, findConnectorByID } from "@common/data/entities/connector/ConnectorUtils";
import { Project } from "@common/data/entities/project/Project";
import { ProjectUploadState } from "@common/data/entities/project/ProjectExternalState.ts";
import { ProjectStatistics } from "@common/data/entities/project/ProjectStatistics";
import { errorMessageDialog } from "@common/ui/dialogs/MessageDialog";
import { finishSentence, formatLocaleTimestamp } from "@common/utils/Strings";

import { FrontendComponent } from "@/component/FrontendComponent";
import { findConnectorCategory } from "@/data/entities/connector/ConnectorUtils";
import { getActiveProjectJob } from "@/data/entities/project/ProjectJobUtils";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useProjectsStore } from "@/data/stores/ProjectsStore.ts";
import { useUserStore } from "@/data/stores/UserStore";
import { InitiateProjectJobAction } from "@/ui/actions/project/InitiateProjectJobAction";
import { ListProjectJobsAction } from "@/ui/actions/project/ListProjectJobsAction";

const comp = FrontendComponent.inject();
const projectsStore = useProjectsStore();
const consStore = useConnectorsStore();
const userStore = useUserStore();
const props = defineProps({
    project: {
        type: Object as PropType<Project>,
        required: true
    },
    instance: {
        type: Object as PropType<ConnectorInstance>,
        required: true
    }
});

const { project, instance } = toRefs(props);
const { volatileStates } = storeToRefs(projectsStore);
const { userAuthorizations } = storeToRefs(userStore);

const connector = computed(() => findConnectorByID(consStore.connectors, unref(instance)!.connector_id));
const uploadOnce = computed(() => (unref(connector)!.options & ConnectorOptions.UploadOnce) == ConnectorOptions.UploadOnce);
const requiresAuth = computed(() => connectorRequiresAuthorization(unref(connector)!));
const isAuthorized = computed(() => connectorInstanceIsAuthorized(unref(instance)!, unref(userAuthorizations)));
const category = unref(connector) ? findConnectorCategory(unref(connector)!) : undefined;

const activeJob = computed(() => getActiveProjectJob(unref(project)!, unref(instance)!));
const uploadState = computed(
    () => unref(volatileStates).findState(unref(project)!.project_id, unref(instance)!.instance_id)?.externalState.external_state || ProjectUploadState.Unknown
);
const jobStats = computed(() => new ProjectStatistics(unref(project)!).getJobStatistics(unref(instance)!.instance_id));

const initiateUpload = ref(false);
const disableUpload = computed(() => {
    if (unref(uploadState) != ProjectUploadState.Default && unref(uploadState) != ProjectUploadState.Uploaded) {
        return true;
    }
    if (unref(connector)) {
        return (unref(uploadOnce) && unref(jobStats).totalCount.succeeded >= 1) || (unref(requiresAuth) && !unref(isAuthorized));
    }
    return true;
});
const disableReason = computed(() => {
    if (unref(uploadOnce) || unref(uploadState) == ProjectUploadState.Locked) {
        return "The project has already been " + category?.verbStatusDone.toLowerCase() + " and is now locked";
    } else if (unref(uploadState) == ProjectUploadState.Unknown) {
        return "Retrieving current project state...";
    } else if (unref(requiresAuth)) {
        return "The connector has not been configured yet";
    }
    return "";
});
const uploadTitle = computed(() => (unref(initiateUpload) ? "Initiating..." : category?.verbAction));

function onUpload() {
    const conn = unref(connector);
    if (conn) {
        initiateUpload.value = true;

        const action = new InitiateProjectJobAction(comp);
        action
            .prepare(unref(project), conn, unref(instance))
            .done((_, success, msg) => {
                onUploadInitDone(success, msg);
            })
            .failed((_, msg) => {
                onUploadInitDone(false, msg);
            });
        action.execute();
    }
}

function onUploadInitDone(success: boolean, msg: string): void {
    // Only unlock the init-phase after updating the jobs list
    const listJobsAction = new ListProjectJobsAction(comp);
    listJobsAction.prepare().done(() => {
        initiateUpload.value = false;
    });
    listJobsAction.execute();

    if (!success) {
        errorMessageDialog(comp, `Unable to start ${category?.verbNoun.toLowerCase() || "job"}`, finishSentence(msg));
    }
}
</script>

<template>
    <div
        class="grid grid-rows-auto gap-2.5 place-content-start group w-full min-h-20"
        :class="activeJob ? 'grid-cols-[min-content_1fr_40%]' : 'grid-cols-[min-content_1fr_max-content]'"
    >
        <div :class="{ 'pt-1': instance!.description }">
            <Tag v-if="!disableUpload" :severity="activeJob ? 'info' : 'success'" :title="activeJob ? 'In progress' : 'Ready'" class="w-10 h-10 rounded-full">
                <span class="material-icons-outlined" :class="activeJob ? 'mi-rocket-launch' : 'mi-rocket'" />
            </Tag>
            <Tag v-else severity="warn" title="Not ready" class="w-10 h-10 rounded-full">
                <span class="material-icons-outlined mi-clear" />
            </Tag>
        </div>

        <div class="grid grid-flow-row content-center">
            <div :id="'connector-instance-' + instance!.instance_id" class="r-text-caption h-6 truncate" :title="instance!.name">{{ instance!.name }}</div>
            <div v-if="instance!.description" class="truncate" :title="instance!.description">{{ instance!.description }}</div>
        </div>

        <div class="row-span-3 pl-1 content-center w-full">
            <div v-if="activeJob" class="grid grid-flow-row text-sm">
                <span class="r-text-light italic justify-self-end w-full truncate" :title="activeJob.message">
                    <b>{{ category?.verbStatusProgressing }}:</b><br />{{ activeJob.message }}
                </span>
                <ProgressBar class="h-3" :value="Math.trunc(activeJob.progress * 100)" :title="activeJob.message" />
            </div>
            <div
                v-else
                :title="disableUpload ? 'Unable to ' + category?.verbAction.toLowerCase() + ': ' + disableReason : category?.verbAction + ' the project'"
            >
                <Button
                    v-if="!disableUpload && category"
                    :label="uploadTitle"
                    :aria-label="uploadTitle"
                    :loading="initiateUpload"
                    size="small"
                    icon="material-icons-outlined mi-rocket-launch"
                    loading-icon="material-icons-outlined mi-rocket-launch"
                    :pt="{ root: category.buttonClass }"
                    @click="onUpload"
                />
                <div v-else class="text-sm r-text-warning">
                    <span class="font-bold">Unable to {{ category?.verbAction.toLowerCase() }}:<br /></span>
                    <span>{{ disableReason }}</span>
                </div>
            </div>
        </div>

        <div class="h-3">&nbsp;</div>

        <div class="grid grid-cols-[1fr_max-content] grid-flow-col col-span-2 text-sm">
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
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
