<script setup lang="ts">
import { storeToRefs } from "pinia";
import { computed, type PropType, ref, toRefs, unref, watch } from "vue";

import { MetadataProfileContainerRole } from "@common/data/entities/metadata/MetadataProfileContainer";
import { filterContainers, isContainerSelected } from "@common/data/entities/metadata/MetadataProfileContainerUtils";
import { DataManagementPlanFeature } from "@common/data/entities/project/features/DataManagementPlanFeature";
import { Project } from "@common/data/entities/project/Project";
import { getOptionalMetadataProfiles } from "@common/data/entities/project/ProjectUtils.ts";
import { type ProfileID } from "@common/ui/components/propertyeditor/PropertyProfile.ts";
import { PropertyProfileStore } from "@common/ui/components/propertyeditor/PropertyProfileStore";
import { makeDebounce } from "@common/ui/components/propertyeditor/utils/PropertyEditorUtils";

import PropertyEditor from "@common/ui/components/propertyeditor/PropertyEditor.vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useMetadataStore } from "@/data/stores/MetadataStore";
import { useUserStore } from "@/data/stores/UserStore.ts";
import { UpdateProjectFeaturesAction } from "@/ui/actions/project/UpdateProjectFeaturesAction";

import MetadataProfilesSelector from "@/ui/components/metadata/MetadataProfilesSelector.vue";
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
const userStore = useUserStore();
const { userSettings } = storeToRefs(userStore);

const enabledProfiles = ref<ProfileID[]>(unref(project).features.dmp.enabled_metadata_profiles);
const metadataProfiles = computed(() => {
    const profileStore = new PropertyProfileStore();

    for (const profile of filterContainers(metadataStore.profiles, DataManagementPlanFeature.FeatureID, [
        MetadataProfileContainerRole.Default,
        MetadataProfileContainerRole.Optional
    ])) {
        if (isContainerSelected(profile, unref(enabledProfiles))) {
            profileStore.mountProfile(profile.profile);
        }
    }

    return profileStore;
});
const optionalProfiles = computed(() =>
    getOptionalMetadataProfiles(unref(project), unref(userSettings), [], metadataStore.profiles, DataManagementPlanFeature.FeatureID)
);

const debounce = makeDebounce();

function saveProject(): void {
    debounce(() => {
        const action = new UpdateProjectFeaturesAction(comp);
        action.prepare(unref(project), [new DataManagementPlanFeature(unref(project).features.dmp.plan, unref(enabledProfiles))]);
        action.execute();
    });
}

watch(() => unref(project).features.dmp.plan, saveProject, { deep: true });
watch(enabledProfiles, saveProject);
</script>

<template>
    <div>
        <div class="grid grid-cols-[1fr_max-content] gap-10 px-1 pt-1 h-min">
            <MetadataProfilesSelector
                v-if="optionalProfiles.length > 0"
                :profiles="optionalProfiles"
                v-model:selected-profiles="enabledProfiles"
                class="h-min"
            />
            <div v-else>&nbsp;</div>

            <ProjectExportersBar :project="project" :scope="DataManagementPlanFeature.FeatureID" class="p-2 grid justify-end" />
        </div>
        <PropertyEditor
            v-model="project.features.dmp.plan"
            v-model:shared-property-objects="project.features.shared_objects"
            :projectProfiles="metadataProfiles"
        />
    </div>
</template>

<style scoped lang="scss"></style>
