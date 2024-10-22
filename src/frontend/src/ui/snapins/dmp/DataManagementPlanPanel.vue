<script setup lang="ts">
import { type PropType, reactive, toRefs, watch } from "vue";

import { MetadataProfileContainerRole } from "@common/data/entities/metadata/MetadataProfileContainer";
import { filterContainers } from "@common/data/entities/metadata/MetadataProfileContainerUtils";
import { type DataManagementPlan, DataManagementPlanFeature } from "@common/data/entities/project/features/DataManagementPlanFeature";
import { Project } from "@common/data/entities/project/Project";
import PropertyEditor from "@common/ui/components/propertyeditor/PropertyEditor.vue";
import { PropertyProfileStore } from "@common/ui/components/propertyeditor/PropertyProfileStore";
import { makeDebounce } from "@common/ui/components/propertyeditor/utils/PropertyEditorUtils";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useMetadataStore } from "@/data/stores/MetadataStore";
import { UpdateProjectFeaturesAction } from "@/ui/actions/project/UpdateProjectFeaturesAction";
import ProjectExportersBar from "@/ui/components/project/ProjectExportersBar.vue";

const comp = FrontendComponent.inject();
const props = defineProps({
    project: {
        type: Object as PropType<Project>,
        required: true
    }
});
const { project } = toRefs(props);
const metadataStore = useMetadataStore();

const debounce = makeDebounce();

const projectProfiles = reactive(new PropertyProfileStore());

watch(
    () => project!.value.features.dmp.plan,
    (dmpSet) => {
        debounce(() => {
            const action = new UpdateProjectFeaturesAction(comp);
            action.prepare(project!.value, [new DataManagementPlanFeature(dmpSet as DataManagementPlan)]);
            action.execute();
        });
    },
    { deep: true }
);

for (const profile of filterContainers(metadataStore.profiles, DataManagementPlanFeature.FeatureID, MetadataProfileContainerRole.Global)) {
    projectProfiles.mountProfile(profile.profile);
}
</script>

<template>
    <ProjectExportersBar :project="project" :scope="DataManagementPlanFeature.FeatureID" class="p-2 grid justify-end" />
    <PropertyEditor
        v-model="project!.features.dmp.plan"
        v-model:shared-objects="project!.features.project_metadata.shared_objects"
        :projectProfiles="projectProfiles as PropertyProfileStore"
    />
</template>

<style scoped lang="scss"></style>
