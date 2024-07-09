<script setup lang="ts">
import { reactive, toRefs, watch, type PropType } from "vue";

import { DataManagementPlanFeature, type DataManagementPlan } from "@common/data/entities/project/features/DataManagementPlanFeature";
import { Project } from "@common/data/entities/project/Project";
import { type ExporterID } from "@common/ui/components/propertyeditor/exporters/Exporter";
import { ProjectObjectStore } from "@common/ui/components/propertyeditor/ProjectObjectStore";
import { type Profile } from "@common/ui/components/propertyeditor/PropertyProfile";
import { PropertyProfileStore } from "@common/ui/components/propertyeditor/PropertyProfileStore";
import { PersistedSet } from "@common/ui/components/propertyeditor/PropertySet";
import { makeDebounce } from "@common/ui/components/propertyeditor/utils/PropertyEditorUtils";

import { dfgDmp } from "@common/ui/components/propertyeditor/profiles/dfg";
import PropertyEditor from "@common/ui/components/propertyeditor/PropertyEditor.vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { UpdateProjectFeaturesAction } from "@/ui/actions/project/UpdateProjectFeaturesAction";

const comp = FrontendComponent.inject();
const props = defineProps({
    project: {
        type: Object as PropType<Project>,
        required: true
    },
    globalObjectStore: {
        type: Object as PropType<ProjectObjectStore>,
        required: true
    }
});
const { project } = toRefs(props);

// TODO: Testing data only
const exporters: ExporterID[] = ["pdf", "raw"];

const projectObjects = reactive(new ProjectObjectStore());
const projectProfiles = reactive(new PropertyProfileStore());
const debounce = makeDebounce(500);

watch(
    () => project!.value.features.dmp.plan,
    (dmpSet: PersistedSet[]) => {
        debounce(() => {
            const action = new UpdateProjectFeaturesAction(comp);
            action.prepare(project!.value, [new DataManagementPlanFeature(dmpSet as DataManagementPlan)]);
            action.execute();
        });
    },
    { deep: true }
);

projectProfiles.mountProfile(dfgDmp as Profile);
</script>

<template>
    <PropertyEditor
        v-model="project!.features.dmp.plan"
        :projectObjects="projectObjects as ProjectObjectStore"
        :globalObjectStore="globalObjectStore as ProjectObjectStore"
        :projectProfiles="projectProfiles as PropertyProfileStore"
    />
</template>

<style scoped lang="scss"></style>
