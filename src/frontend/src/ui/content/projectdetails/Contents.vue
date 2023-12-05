<script setup lang="ts">
import TabPanel from "primevue/tabpanel";
import TabView from "primevue/tabview";
import { computed, toRefs } from "vue";

import { Project } from "@common/data/entities/Project";
import { ProjectFeatureFlags } from "@common/features/ProjectFeature";
import { ProjectFeaturesCatalog } from "@common/features/ProjectFeaturesCatalog";

const props = defineProps({
    project: {
        type: Project,
        required: true
    }
});
const { project } = toRefs(props);

const panels = computed(() => {
    // Select all features that provide a panel and are either non-optional or turned on by the user
    const panelFeatures = ProjectFeaturesCatalog.filter(ProjectFeatureFlags.HasPanel)
        .filter((feature) => !feature.hasFlags(ProjectFeatureFlags.Optional) || project!.value.features_selection.includes(feature.featureID));
    return panelFeatures.map((feature) => {
        return { title: feature.displayName, component: feature.panel };
    });
});
</script>

<template>
    <div>
        <TabView select-on-focus :pt="{
            nav: 'tab-view'
        }">
            <TabPanel v-for="panel in panels" :key="panel.title" :header="panel.title" :pt="{
                header: 'tab-view-panel',
                headerAction: 'tab-view-panel-action'
            }">
                <component :is="panel.component" />
            </TabPanel>
        </TabView>
    </div>
</template>

<style scoped lang="scss">
:deep(.tab-view) {
    @apply bg-[var(--r-shade)];
}

:deep(.tab-view-panel) {
    @apply bg-[var(--r-shade)] w-full border-e-2 #{!important};
}

:deep(.tab-view-panel-action) {
    @apply bg-[var(--r-shade)] place-content-center #{!important};
}
</style>
