<script setup lang="ts">
import { reactive, toRefs } from "vue";

import logging from "@common/core/logging/Logging";
import { Project } from "@common/data/entities/project/Project";
import { type DataManagementPlan, DataManagementPlanFeature } from "@common/data/entities/project/features/DataManagementPlanFeature";
import { type ExporterID } from "@common/ui/components/propertyeditor/exporters/Exporter";
import { DmpController } from "@common/ui/components/propertyeditor/PropertyController";
import { PersistedSet, PropertySet } from "@common/ui/components/propertyeditor/PropertySet";
import { extractPersistedSetFromArray } from "@common/ui/components/propertyeditor/utils/PropertyEditorUtils";

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

const handleDMPUpdate = (data: PersistedSet[]) => {
    const dmpSet = extractPersistedSetFromArray(data, dfgDmp.profile_id);
    const action = new UpdateProjectFeaturesAction(comp);
    action.prepare(project!.value, [new DataManagementPlanFeature(dmpSet as DataManagementPlan)]);
    action.execute();

    // TODO: Just a quick hack, perform update in a better way later
    // @ts-ignore
    project!.value.features.dmp.plan = dmpSet;
};
</script>

<template>
    <PropertyEditor
        @update="handleDMPUpdate"
        :controller="controller"
        :logging="logging"
        :exporters="exporters"
        :project="project"
        oneCol
    />
</template>

<style scoped lang="scss"></style>
