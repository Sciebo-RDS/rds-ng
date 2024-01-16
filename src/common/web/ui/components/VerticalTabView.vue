<script setup lang="ts">
import { toRefs } from "vue";
import TabPanel from "primevue/tabpanel";
import TabView from "primevue/tabview";

import { type VerticalTabDefinition } from "./VerticalTabView";

const props = defineProps({
    tabs: {
        type: Object as [VerticalTabDefinition],
        required: true
    },
    tabData: {}
});
const { tabs, tabData } = toRefs(props);
</script>

<template>
    <TabView select-on-focus :pt="{
            root: 'tab-view',
            nav: 'tab-view-nav',
            navContent: 'tab-view-nav-content',
            panelContainer: 'tab-view-panels'
        }">
        <TabPanel v-for="tab in tabs" :key="tab.title" :header="tab.title" :pt="{
                header: 'tab-view-panel',
                headerAction: 'tab-view-panel-action'
            }">
            <component :is="tab.component" :tabData="tabData" />
        </TabPanel>
    </TabView>
</template>

<style scoped lang="scss">
:deep(.tab-view) {
    @apply flex;
}

:deep(.tab-view-nav) {
    @apply block border-none #{!important};
}

:deep(.tab-view-nav-content) {
    @apply float-left pr-10;
}

:deep(.tab-view-panels) {
    @apply p-0;
}

:deep(.tab-view-panel) {
    @apply w-full #{!important};
}

:deep(.tab-view-panel-action:focus) {
    @apply shadow-none #{!important};
}

:deep(.tab-view-panel-action) {
    @apply place-content-start border-none rounded-none p-0 mb-5 #{!important};
}
</style>
