<script setup lang="ts">
import TabPanel from "primevue/tabpanel";
import TabView from "primevue/tabview";
import { computed, defineAsyncComponent, toRefs } from "vue";

import { Project } from "@common/data/entities/project/Project";

import { type UIOptions } from "@/data/entities/UIOptions";
import { SnapInsCatalog } from "@/ui/snapins/SnapInsCatalog";

const props = defineProps({
    project: {
        type: Project,
        required: true
    }
});
const { project } = toRefs(props);

const panels = computed(() => {
    // Select all snap-ins that provide a tab panel and are either non-optional or turned on by the user
    const panelSnapIns = SnapInsCatalog.allWithTabPanel().filter(
        (snapIn) => {
            const uiOptions = project!.value.options.ui as UIOptions;
            return !snapIn.isOptional() || uiOptions.optional_snapins?.includes(snapIn.snapInID);
        }
    );
    return panelSnapIns.map((snapIn) => {
        return { title: snapIn.options.tabPanel!.label, component: defineAsyncComponent(snapIn.options.tabPanel!.loader) };
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
                <component :is="panel.component" :project="project" />
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
