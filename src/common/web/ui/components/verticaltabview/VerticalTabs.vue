<script setup lang="ts">
import { type PropType, toRefs } from "vue";
import Tabs from "primevue/tabs";
import TabList from "primevue/tablist";
import Tab from "primevue/tab";
import TabPanels from "primevue/tabpanels";
import TabPanel from "primevue/tabpanel";

import { type VerticalTabDefinition } from "./VerticalTabs";

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
    <Tabs v-model:value="activeTab" class="h-full" :pt="{ root: 'grid grid-flow-col' }">
        <TabList :pt="{ tabList: 'tab-list', activeBar: 'tab-list-active-bar' }">
            <Tab v-for="[index, tab] of tabs.entries()" :value="index" class="tab">
                <div class="flex items-center gap-1.5">
                    <span v-if="tab.icon" :class="'material-icons-outlined ' + tab.icon" style="font-size: 1rem" />
                    <span>{{ tab.title }}</span>
                </div>
            </Tab>
        </TabList>
        <TabPanels class="tab-panels">
            <TabPanel v-for="[index, tab] of tabs.entries()" :value="index" class="tab-panel">
                <component :is="tab.component" :tab-data="tabData" />
            </TabPanel>
        </TabPanels>
    </Tabs>
</template>

<style scoped lang="scss">
:deep(.tab-list) {
    @apply grid grid-flow-row border-0 pt-1;
}

:deep(.tab-list-active-bar) {
    @apply hidden;
}

:deep(.tab) {
    @apply border-0 p-0 pr-10 pb-5;
}

:deep(.tab-panels) {
    @apply p-0 flex;
}

:deep(.tab-panel) {
    @apply w-full;
}
</style>
