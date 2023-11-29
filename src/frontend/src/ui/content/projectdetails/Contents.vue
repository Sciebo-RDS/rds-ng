<script setup lang="ts">
import TabPanel from "primevue/tabpanel";
import TabView from "primevue/tabview";
import { toRefs } from "vue";

import { Project } from "@common/data/entities/Project";

const props = defineProps({
    project: {
        type: Project
    }
});
const { project } = toRefs(props);

import { ref } from "vue";

const tabs = ref([
    { title: "Metadata", content: "Tab 1 Content" },
    { title: "Data Management Plan", content: "Tab 2 Content" },
    { title: "Summary", content: "Tab 3 Content" }
]);
</script>

<template>
    <div>
        <TabView select-on-focus :pt="{
            nav: 'tab-view'
        }">
            <TabPanel v-for="tab in tabs" :key="tab.title" :header="tab.title" :pt="{
                header: 'tab-view-panel',
                headerAction: 'tab-view-panel'
            }">
                <p class="m-0">{{ tab.content }}</p>
            </TabPanel>
        </TabView>
    </div>
</template>

<style scoped lang="scss">
:deep(.tab-view) {
    @apply bg-[var(--r-shade)];
}

:deep(.tab-view-panel) {
    @apply bg-[var(--r-shade)] #{!important};
}
</style>
