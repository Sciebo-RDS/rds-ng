<script setup lang="ts">
import { reactive, toRefs, watch, type PropType } from "vue";

import { DataManagementPlanFeature, type DataManagementPlan } from "@common/data/entities/project/features/DataManagementPlanFeature";
import { Project } from "@common/data/entities/project/Project";
import { type ExporterID } from "@common/ui/components/propertyeditor/exporters/Exporter";
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
    }
});
const { project } = toRefs(props);

// TODO: Testing data only
const exporters: ExporterID[] = ["pdf", "raw"];

const debounce = makeDebounce(500);

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

projectProfiles.mountProfile(dfgDmp as Profile);
</script>

<template>
    <div>
        <PropertyEditor
            v-model="project!.features.dmp.plan"
            v-model:shared-objects="project!.features.metadata.shared_objects"
            :projectProfiles="projectProfiles as PropertyProfileStore"
        />
    </div>
</template>

<style scoped lang="scss"></style>
