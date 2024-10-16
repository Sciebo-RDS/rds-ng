<script setup lang="ts">
import { saveAs } from "file-saver";
import Button from "primevue/button";
import ButtonGroup from "primevue/buttongroup";
import sanitize from "sanitize-filename";
import { computed, type PropType, ref } from "vue";

import { ExportProjectReply } from "@common/api/project/ProjectExportersCommands";
import { Project } from "@common/data/entities/project/Project";
import { ProjectExporterDescriptor } from "@common/data/exporters/ProjectExporterDescriptor";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useProjectExportersStore } from "@/data/stores/ProjectExportersStore";
import { ExportProjectAction } from "@/ui/actions/project/ExportProjectAction";

const comp = FrontendComponent.inject();
const props = defineProps({
    project: {
        type: Object as PropType<Project>,
        required: true
    },
    scope: {
        type: String,
        default: ""
    }
});

const { exporters } = useProjectExportersStore();
const availableExporters = computed(() => exporters.filter((exporter) => props.scope == "" || exporter.scope.includes(props.scope)).sort());

const exportRunning = ref(false);

function onExport(exporter: ProjectExporterDescriptor): void {
    exportRunning.value = true;

    const action = new ExportProjectAction(comp);
    action
        .prepare(props.project, exporter, props.scope)
        .done((reply: ExportProjectReply, success: boolean, _: string) => {
            const filename = sanitize(`${props.project.title}.${props.scope}.${exporter.extension}`);
            saveAs(new Blob([reply.data!], { type: reply.mimetype }), filename);

            exportRunning.value = false;
        })
        .failed(() => {
            exportRunning.value = false;
        });
    action.execute();
}
</script>

<template>
    <div v-if="availableExporters.length > 0" class="grid grid-flow-col gap-1.5 items-center p-0 text-xs">
        <span class="flex items-center gap-0.5 text-sm">
            <span class="material-icons-outlined" :class="exportRunning ? 'mi-hourglass-empty animate-spin' : 'mi-file-download'" />
            <span class="font-bold pr-1">Export</span>
        </span>
        <ButtonGroup>
            <Button
                v-for="exporter in availableExporters"
                :label="exporter.name"
                :title="exporter.description"
                size="small"
                :disabled="exportRunning"
                @click="onExport(exporter)"
            />
        </ButtonGroup>
    </div>
</template>

<style scoped lang="scss"></style>
