<script setup lang="ts">
import Panel from "primevue/panel";
import { type PropType, toRefs } from "vue";

import { Project } from "@common/data/entities/project/Project";

import ObjectsPanel from "@/ui/snapins/summary/ObjectsPanel.vue";
import ProjectPanel from "@/ui/snapins/summary/ProjectPanel.vue";
import TimelinePanel from "@/ui/snapins/summary/TimelinePanel.vue";

const props = defineProps({
    project: {
        type: Object as PropType<Project>,
        required: true,
    },
});
const { project } = toRefs(props);
</script>

<template>
    <div class="grid grid-rows-[auto_1fr] gap-3.5 p-3.5 h-full">
        <Panel :header="project.title" class="r-shade-gray" :pt="{ title: 'text-xl' }">
            <ProjectPanel :project="project" />
        </Panel>

        <div class="grid grid-cols-2 gap-3.5">
            <div class="panel-container">
                <Panel
                    header="Timeline"
                    class="panel-container-content r-shade-gray"
                    :pt="{ title: 'text-xl', toggleableContent: 'h-[calc(100%-4rem)]', content: 'h-full' }"
                >
                    <TimelinePanel :project="project" />
                </Panel>
            </div>

            <div class="panel-container">
                <Panel
                    header="Object statistics"
                    class="panel-container-content r-shade-gray"
                    :pt="{ title: 'text-xl', toggleableContent: 'h-[calc(100%-4rem)]', content: 'h-full' }"
                >
                    <ObjectsPanel :project="project" />
                </Panel>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">
.panel-container {
    @apply h-full relative;
}

.panel-container-content {
    @apply w-full h-full absolute;
}
</style>
