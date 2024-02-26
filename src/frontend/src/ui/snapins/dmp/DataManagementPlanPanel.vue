<script setup lang="ts">
import { reactive, toRefs, watch } from "vue";

import logging from "@common/core/logging/Logging";
import { Project } from "@common/data/entities/project/Project";
import { type DataManagementPlan, DataManagementPlanFeature } from "@common/data/entities/project/features/DataManagementPlanFeature";
import { type ExporterID } from "@common/ui/components/propertyeditor/exporters/Exporter";
import { DmpController } from "@common/ui/components/propertyeditor/PropertyController";
import { PersistedSet, PropertySet } from "@common/ui/components/propertyeditor/PropertySet";

import { dfgDmp } from "@common/ui/components/propertyeditor/profiles/dfg";
import PropertyEditor from "@common/ui/components/propertyeditor/PropertyEditor.vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { UpdateProjectFeaturesAction } from "@/ui/actions/project/UpdateProjectFeaturesAction";

const comp = FrontendComponent.inject();
const props = defineProps({
    project: {
        type: Project,
        required: true
    }
});
const { project } = toRefs(props);

// TODO: Testing data only
const exporters: ExporterID[] = ["pdf", "raw"];

const dmpProfile = new PropertySet(dfgDmp, project!.value.features.dmp.plan as PersistedSet);
const controller = reactive(new DmpController(dmpProfile));

watch(project!.value.features.dmp.plan, (dmpSet) => {
    const action = new UpdateProjectFeaturesAction(comp);
    action.prepare(project!.value, [new DataManagementPlanFeature(dmpSet as DataManagementPlan)]);
    action.execute();
});
</script>

<template>
    <PropertyEditor
        v-model="project!.features.dmp.plan"
        :controller="controller as DmpController"
        :logging="logging"
        :exporters="exporters"
        :project="project"
        oneCol
    />
</template>

<style scoped lang="scss"></style>
