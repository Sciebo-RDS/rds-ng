<script setup lang="ts">
import { reactive, ref, toRefs, watch, type PropType } from "vue";

import { DataManagementPlanFeature, type DataManagementPlan } from "@common/data/entities/project/features/DataManagementPlanFeature";
import { MetadataFeature, type ProjectMetadata } from "@common/data/entities/project/features/MetadataFeature";
import { Project } from "@common/data/entities/project/Project";
import { type ExporterID } from "@common/ui/components/propertyeditor/exporters/Exporter";
import { ProjectObjectStore } from "@common/ui/components/propertyeditor/ProjectObjectStore";
import { type Profile } from "@common/ui/components/propertyeditor/PropertyProfile";
import { PropertyProfileStore } from "@common/ui/components/propertyeditor/PropertyProfileStore";
import { makeDebounce } from "@common/ui/components/propertyeditor/utils/PropertyEditorUtils";
import { deepClone } from "@common/utils/ObjectUtils";

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
projectObjects.value.setObjects(deepClone(project!.value.features.dmp.plan));

const sharedObjects = ref(new ProjectObjectStore());
sharedObjects.value.setObjects(deepClone(project!.value.features.metadata.shared_objects));


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

watch(
    () => sharedObjects.value._objects,
    (shared_objects) => {
        debounce(() => {
            const action = new UpdateProjectFeaturesAction(comp);
            action.prepare(project!.value, [new MetadataFeature(project!.value.features.metadata.metadata as ProjectMetadata, shared_objects)]);
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
