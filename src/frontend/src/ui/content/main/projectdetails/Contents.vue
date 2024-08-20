<script setup lang="ts">
import { makeDebounce } from "@common/ui/components/propertyeditor/utils/PropertyEditorUtils";
import TabPanel from "primevue/tabpanel";
import TabView from "primevue/tabview";
import { computed, defineAsyncComponent, reactive, ref, toRefs, watch } from "vue";

import { Project } from "@common/data/entities/project/Project";

import { FrontendComponent } from "@/component/FrontendComponent";
import { type UIOptions } from "@/data/entities/ui/UIOptions";
import { UpdateProjectFeaturesAction } from "@/ui/actions/project/UpdateProjectFeaturesAction";
import { SnapInsCatalog } from "@/ui/snapins/SnapInsCatalog";
import { MetadataFeature, type ProjectMetadata } from "@common/data/entities/project/features/MetadataFeature";
import { ProjectObjectStore } from "@common/ui/components/propertyeditor/ProjectObjectStore";

const comp = FrontendComponent.inject();
const props = defineProps({
    project: {
        type: Project,
        required: true
    }
});
const { project } = toRefs(props);

const panels = computed(() => {
    // Select all snap-ins that provide a tab panel and are either non-optional or turned on by the user
    const panelSnapIns = SnapInsCatalog.allWithTabPanel().filter((snapIn) => {
        const uiOptions = project!.value.options.ui as UIOptions;
        return !snapIn.isOptional() || uiOptions.optional_snapins?.includes(snapIn.snapInID);
    });
    return panelSnapIns.map((snapIn) => {
        return { title: snapIn.options.tabPanel!.label, component: defineAsyncComponent(snapIn.options.tabPanel!.loader) };
    });
});

const sharedObjectStore = reactive(new ProjectObjectStore());

const debounce = makeDebounce(500);
watch(
    () => project!.value.features.metadata.shared_objects,
    (shared_objects) => {
        debounce(() => {
            const action = new UpdateProjectFeaturesAction(comp);
            action.prepare(project!.value, [
                new MetadataFeature(project!.value.features.metadata.metadata as ProjectMetadata, shared_objects as ProjectMetadata)
            ]);
            action.execute();
        });
    },
    { deep: true }
);
const activeTabIndex = ref(0);

watch(
    () => panels.value,
    (panelsNew, panelsOld) => {
        const newCurrent = panelsNew.findIndex((e) => e === panelsOld[activeTabIndex.value]);
        if (newCurrent !== -1) activeTabIndex.value = newCurrent;
        else activeTabIndex.value = Math.max(0, activeTabIndex.value - 1);
    }
);
</script>
<template>
    <div class="h-full">
        <TabView
            class="h-full"
            :pt="{
                nav: 'tab-view',
                panelContainer: 'overflow-y-auto max-h-[calc(100vh-8.0rem)] p-0 h-full' // TODO: Hacky height
            }"
            :activeIndex="activeTabIndex"
            @update:activeIndex="activeTabIndex = $event"
        >
            <TabPanel
                v-for="panel in panels"
                :key="panel.title"
                :header="panel.title"
                :pt="{
                    header: 'tab-view-panel',
                    headerAction: 'tab-view-panel-action',
                    content: 'h-full'
                }"
            >
                <component :is="panel.component" :project="project" :sharedObjectStore="sharedObjectStore" />
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

:deep(.tab-view-panel-action:focus) {
    @apply shadow-none #{!important};
}
</style>
