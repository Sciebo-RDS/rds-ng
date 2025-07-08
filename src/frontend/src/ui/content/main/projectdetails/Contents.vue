<script setup lang="ts">
import ScrollPanel from "primevue/scrollpanel";
import Tab from "primevue/tab";
import TabList from "primevue/tablist";
import TabPanel from "primevue/tabpanel";
import TabPanels from "primevue/tabpanels";
import Tabs from "primevue/tabs";
import { computed, defineAsyncComponent, type PropType, reactive, ref, toRefs, unref, watch } from "vue";

import { Project } from "@common/data/entities/project/Project";
import { PropertyObjectStore } from "@common/ui/components/propertyeditor/PropertyObjectStore";
import { makeDebounce } from "@common/ui/components/propertyeditor/utils/PropertyEditorUtils";

import LegendHeader from "@common/ui/components/misc/LegendHeader.vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { type UIOptions } from "@/data/entities/ui/UIOptions";
import { UpdateProjectFeaturesAction } from "@/ui/actions/project/UpdateProjectFeaturesAction";
import { SnapInsCatalog } from "@/ui/snapins/SnapInsCatalog";

const comp = FrontendComponent.inject();
const props = defineProps({
    project: {
        type: Object as PropType<Project>,
        required: true
    }
});
const { project } = toRefs(props);

const activePanelIndex = ref(0);
const panels = computed(() => {
    // Select all snap-ins that provide a tab panel and are either non-optional or turned on by the user
    const panelSnapIns = SnapInsCatalog.allWithTabPanel().filter((snapIn) => {
        const uiOptions = project!.value.options.ui as UIOptions;
        return !snapIn.isOptional() || uiOptions.optional_snapins?.includes(snapIn.snapInID);
    });

    if (unref(activePanelIndex) >= panelSnapIns.length) {
        activePanelIndex.value = panelSnapIns.length - 1;
    }

    return panelSnapIns.map((snapIn) => {
        return {
            title: snapIn.options.tabPanel!.label,
            component: defineAsyncComponent(snapIn.options.tabPanel!.loader),
            description: snapIn.options.tabPanel!.description
        };
    });
});

const sharedPropertyObjectStore = reactive(new PropertyObjectStore());
const debounce = makeDebounce();
watch(
    () => project!.value.features.shared_objects,
    (shared_objects) => {
        debounce(() => {
            const action = new UpdateProjectFeaturesAction(comp);
            action.prepare(project!.value, [], shared_objects);
            action.execute();
        });
    },
    { deep: true }
);
</script>

<template>
    <div class="h-full">
        <Tabs :value="panels[0].title" class="h-full">
            <TabList :pt="{ tabList: 'tab-list', activeBar: 'tab-list-active-bar' }">
                <Tab v-for="panel in panels" :value="panel.title" class="tab" :title="panel.description">
                    <LegendHeader :title="panel.title" :description="panel.description" />
                </Tab>
            </TabList>
            <TabPanels class="overflow-y-hidden max-h-[calc(100vh-8.0rem)] p-0 h-full">
                <TabPanel v-for="panel in panels" :value="panel.title" class="h-full">
                    <ScrollPanel class="h-full bg-surface-0">
                        <component :is="panel.component" :project="project" :sharedPropertyObjectStore="sharedPropertyObjectStore" />
                    </ScrollPanel>
                </TabPanel>
            </TabPanels>
        </Tabs>
    </div>
</template>

<style scoped lang="scss">
:deep(.tab-list) {
    @apply grid grid-flow-col bg-surface-50;
}

:deep(.tab-list-active-bar) {
    @apply border border-[var(--p-rds-highlight-500)];
}

:deep(.tab) {
    @apply border-e border-inherit p-3;
}
</style>
