<script setup lang="ts">
import { type PropType, toRefs } from "vue";
import TabPanel from "primevue/tabpanel";
import TabView from "primevue/tabview";

import { type VerticalTabDefinition } from "./VerticalTabView";

const props = defineProps({
    tabs: {
        type: Object as PropType<VerticalTabDefinition[]>,
        required: true
    },
    tabData: {}
});
const { tabs, tabData } = toRefs(props);
const activeTab = defineModel<number>("activeTab", { default: 0 });
</script>

<template>
    <TabView v-model:active-index="activeTab" :pt="{
            root: 'tab-view',
            nav: 'tab-view-nav',
            navContent: 'tab-view-nav-content',
            panelContainer: 'tab-view-panels'
        }">
        <TabPanel v-for="tab in tabs" :key="tab.title" :pt="{
                header: 'tab-view-panel',
                headerAction: 'tab-view-panel-action'
            }">
            <template #header>
                <div class="flex items-center gap-1.5">
                    <span v-if="tab.icon" :class="'material-icons-outlined ' + tab.icon" style="font-size: 1rem;" />
                    <span>{{ tab.title }}</span>
                </div>
            </template>
            <component :is="tab.component" :tab-data="tabData" />
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
    @apply float-left pr-10 pt-1;
}

:deep(.tab-view-panels) {
    @apply p-0 flex;
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
