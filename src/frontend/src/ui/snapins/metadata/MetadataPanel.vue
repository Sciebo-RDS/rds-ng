<script setup lang="ts">
import { reactive, toRefs } from "vue";

import logging from "@common/core/logging/Logging";
import { Project } from "@common/data/entities/project/Project";
import { MetadataFeature, type ProjectMetadata } from "@common/data/entities/project/features/MetadataFeature";
import { testProfile } from "@common/ui/components/propertyeditor/DummyData";
import { dataCite } from "@common/ui/components/propertyeditor/profiles/datacite";
import { osf } from "@common/ui/components/propertyeditor/profiles/osf";
import { MetadataController } from "@common/ui/components/propertyeditor/PropertyController";
import { PersistedSet, PropertySet } from "@common/ui/components/propertyeditor/PropertySet";
import { extractPersistedSetFromArray } from "@common/ui/components/propertyeditor/utils/PropertyEditorUtils";

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
const baseSet = new PropertySet(dataCite, extractPersistedSetFromArray(project!.value.features.metadata.metadata, dataCite.profile_id));
const mergeSet = [new PropertySet(osf, extractPersistedSetFromArray(project!.value.features.metadata.metadata, osf.profile_id))];
const profiles: PropertySet[] = [new PropertySet(testProfile, extractPersistedSetFromArray(project!.value.features.metadata.metadata, testProfile.profile_id))];
const controller = reactive(new MetadataController(baseSet, mergeSet, profiles)) as MetadataController;

const handleMetadataUpdate: Function = (data: PersistedSet) => {
    const metadata = data as ProjectMetadata;
    const action = new UpdateProjectFeaturesAction(comp);
    action.prepare(project!.value, [new MetadataFeature(metadata)]);
    action.execute();

    // TODO: Just a quick hack, perform update in a better way later
    // @ts-ignore
    project!.value.features.metadata.metadata = metadata;
};
</script>

<template>
    <div>
        <PropertyEditor
            @update="handleMetadataUpdate"
            :controller="controller"
            :logging="logging"
            twoCol
        />
    </div>
</template>

<style scoped lang="scss"></style>
