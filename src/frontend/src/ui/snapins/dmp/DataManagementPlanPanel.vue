<script setup lang="ts">
import { toRefs, reactive } from "vue";

import { Project } from "@common/data/entities/project/Project";
import { DmpController } from "@common/ui/components/propertyeditor/PropertyController";
import { dfgDmp } from "@common/ui/components/propertyeditor/profiles/dfg";
import { PropertySet } from "@common/ui/components/propertyeditor/PropertySet";
import PropertyEditor from "@common/ui/components/propertyeditor/PropertyEditor.vue";
import logging from "@common/core/logging/Logging";
import { type ExporterID } from "@common/ui/components/propertyeditor/Exporter";

const props = defineProps({
    project: {
        type: Project,
        required: true,
    },
});
const { project } = toRefs(props);

/* Testdata */
const exporters: ExporterID[] = ["pdf", "raw"];
const dmpProfile: PropertySet = new PropertySet(dfgDmp);

const controller = reactive(new DmpController(dmpProfile));

const handleDmpUpdate: Function = (data: any) => {
    logging.debug(`Received update from PropertyEditor: ${JSON.stringify(data)}`, "ProjectDetails");
};
</script>

<template>
    <div v-if="!!controller">
        <PropertyEditor
            @update="(data: any) => handleDmpUpdate(data)"
            :controller="controller"
            :logging="logging"
            :exporters="exporters"
            :project="project"
            oneCol
        />
    </div>
    <div v-else>... and I am the humble DMP ...</div>
</template>

<style scoped lang="scss"></style>
