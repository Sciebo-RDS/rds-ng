<script setup lang="ts">
import { storeToRefs } from "pinia";
import Badge from "primevue/badge";
import Button from "primevue/button";
import OverlayPanel from "primevue/overlaypanel";
import { computed, ref, unref } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { getUnseenProjectJobHistoryRecords } from "@/data/entities/project/ProjectUtils";
import { useProjectJobsStore } from "@/data/stores/ProjectJobsStore";
import { useProjectsStore } from "@/data/stores/ProjectsStore";
import { useUserStore } from "@/data/stores/UserStore";

import { useUserTools } from "@/ui/tools/user/UserTools";

import ProjectJobsPanel from "@/ui/content/main/jobspanel/ProjectJobsPanel.vue";

const comp = FrontendComponent.inject();
const projStore = useProjectsStore();
const projJobsStore = useProjectJobsStore();
const userStore = useUserStore();
const { projects } = storeToRefs(projStore);
const { jobs } = storeToRefs(projJobsStore);
const { userToken, userSettings } = storeToRefs(userStore);
const { editUserSettings } = useUserTools(comp);

const jobsPanel = ref();
const jobsPanelIcon = computed(() => (unref(jobs).length ? "material-icons-outlined mi-rocket-launch -rotate-45" : "material-icons-outlined mi-rocket"));
const jobsPanelBadgeVisible = computed(() => unref(projects).find((project) => getUnseenProjectJobHistoryRecords(project).length > 0));

function onShowJobsPanel(event: Event): void {
    unref(jobsPanel).toggle(event);
}

function onEditUserSettings(): void {
    editUserSettings(userSettings.value);
}
</script>

<template>
    <div class="grid grid-rows-2 grid-cols-[min-content_1fr_max-content] grid-flow-col gap-x-2 content-center items-center r-primary-bg r-primary-text">
        <div class="row-span-2">
            <a href="https://www.research-data-services.org" target="_blank">
                <img id="logo" src="@assets/img/rds-octopus-wh.svg" alt="RDS Logo" class="p-1.5" title="Visit the RDS website" />
            </a>
        </div>

        <div class="font-bold self-center pt-3">
            <div v-if="userToken" :title="userToken.user_id">{{ userToken.user_name }}</div>
            <div v-else>(No user logged in)</div>
        </div>

        <div class="italic self-center pb-3">
            <div v-if="projects.length > 1">{{ projects.length }} projects</div>
            <div v-else-if="projects.length == 1">{{ projects.length }} project</div>
            <div v-else>No projects</div>
        </div>

        <div class="row-span-2 flex gap-x-1 pr-2">
            <div>
                <Button
                    plain
                    rounded
                    aria-label="Jobs"
                    title="Jobs"
                    :icon="jobsPanelIcon"
                    icon-class="r-primary-text !text-4xl"
                    class="size-12 p-overlay-badge"
                    @click="onShowJobsPanel"
                />
                <Badge severity="danger" class="float-left relative top-3/4 left-3/4" :class="{ hidden: !jobsPanelBadgeVisible }" />
            </div>

            <Button
                plain
                rounded
                aria-label="Settings"
                title="Settings"
                icon="material-icons-outlined mi-settings"
                icon-class="r-primary-text !text-4xl"
                class="size-12"
                @click="onEditUserSettings"
            />
        </div>

        <OverlayPanel ref="jobsPanel">
            <ProjectJobsPanel :projects="projects" :jobs="jobs" />
        </OverlayPanel>
    </div>
</template>

<style scoped lang="scss">
#logo {
    min-width: 5rem;
}
</style>
