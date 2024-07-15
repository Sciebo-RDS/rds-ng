<script setup lang="ts">
import { reactive, ref, toRefs, watch, type PropType } from "vue";

import { DataManagementPlanFeature, type DataManagementPlan } from "@common/data/entities/project/features/DataManagementPlanFeature";
import { Project } from "@common/data/entities/project/Project";
import { type ExporterID } from "@common/ui/components/propertyeditor/exporters/Exporter";
import { ProjectObject, ProjectObjectStore } from "@common/ui/components/propertyeditor/ProjectObjectStore";
import { type Profile } from "@common/ui/components/propertyeditor/PropertyProfile";
import { PropertyProfileStore } from "@common/ui/components/propertyeditor/PropertyProfileStore";
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
    sharedObjectStore: {
        type: Object as PropType<ProjectObjectStore>,
        required: true
    }
});
const { project } = toRefs(props);

// TODO: Testing data only
const exporters: ExporterID[] = ["pdf", "raw"];

const debounce = makeDebounce(500);

const projectProfiles = reactive(new PropertyProfileStore());

const projectObjects = ref(new ProjectObjectStore());
projectObjects.value.setObjects(project!.value.features.dmp.plan as ProjectObject[]);

const sharedObjects = ref(new ProjectObjectStore());
sharedObjects.value.setObjects(project!.value.features.metadata.shared_objects as ProjectObject[]);

watch(
    () => projectObjects.value._objects,
    (dmpSet) => {
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
        v-model="projectObjects as ProjectObjectStore"
        v-model:shared-objects="sharedObjects as ProjectObjectStore"
        :projectProfiles="projectProfiles as PropertyProfileStore"
    />
</template>

<style scoped lang="scss"></style>
