<script setup lang="ts">
import { storeToRefs } from "pinia";
import { computed } from "vue";

import { DisplayState, useFrontendStore } from "@/data/stores/FrontendStore.ts";
import { useProjectsStore } from "@/data/stores/ProjectsStore";

import Contents from "@/ui/content/main/projectdetails/Contents.vue";
import ContentsLanding from "@/ui/content/main/projectdetails/ContentsLanding.vue";
import Header from "@/ui/content/main/projectdetails/Header.vue";
import HeaderEmpty from "@/ui/content/main/projectdetails/HeaderEmpty.vue";

const frontendStore = useFrontendStore();
const projStore = useProjectsStore();

const { displayState } = storeToRefs(frontendStore);
const currentProject = computed(() => projStore.resolveActiveProject());
</script>

<template>
    <div v-if="displayState == DisplayState.Project && !!currentProject" class="contents">
        <Header :project="currentProject" />
        <Contents :project="currentProject" />
    </div>
    <div v-else class="contents">
        <HeaderEmpty />
        <ContentsLanding />
    </div>
</template>

<style scoped lang="scss">
.contents {
    @apply grid grid-rows-[4rem_1fr] grid-cols-1 gap-0 w-full h-full;
}
</style>
