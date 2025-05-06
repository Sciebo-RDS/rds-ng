<script setup lang="ts">
import { storeToRefs } from "pinia";
import OverlayBadge from "primevue/overlaybadge";
import Button from "primevue/button";
import Popover from "primevue/popover";
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
const { projects, activeProject } = storeToRefs(projStore);
const { jobs } = storeToRefs(projJobsStore);
const { userToken, userSettings } = storeToRefs(userStore);
const { editUserSettings } = useUserTools(comp);

const jobsPanel = ref();
const jobsPanelIcon = computed(() => (unref(jobs).length ? "material-icons-outlined mi-rocket-launch -rotate-45" : "material-icons-outlined mi-rocket"));
const jobPanelBadgeCounter = computed(() => {
    let count: number = unref(jobs).length;
    count += unref(projects)
        .map((project) => getUnseenProjectJobHistoryRecords(project).length)
        .reduce((v, acc) => v + acc, 0);
    return count;
});

function onGoHome(): void {
    activeProject.value = undefined;
    comp.userInterface.frontendView.navigateTo(true, undefined, { project_id: undefined });
}

function onShowJobsPanel(event: Event): void {
    unref(jobsPanel).toggle(event);
}

function onEditUserSettings(): void {
    editUserSettings(userSettings.value);
}
</script>

<template>
    <div class="grid grid-rows-2 grid-cols-[min-content_1fr_max-content] grid-flow-col gap-y-3 content-center items-center r-primary-bg r-primary-text">
        <div class="row-span-2">
            <a href="#" @click.prevent="onGoHome">
                <img id="logo" src="@assets/img/rds-octopus-wh.svg" alt="RDS Logo" class="p-3" title="Home" />
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
                    class="size-12"
                    @click="onShowJobsPanel"
                />
                <OverlayBadge
                    severity="danger"
                    class="inset-[-0.3rem] pt-px"
                    :class="{ hidden: jobPanelBadgeCounter <= 0 }"
                    size="small"
                    :value="jobPanelBadgeCounter < 9 ? jobPanelBadgeCounter : '9+'"
                    :title="jobPanelBadgeCounter"
                    :dt="{ 'outline.width': 0, 'font.weight': '800' }"
                />
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

        <Popover ref="jobsPanel">
            <ProjectJobsPanel :projects="projects" :jobs="jobs" />
        </Popover>
    </div>
</template>

<style scoped lang="scss">
#logo {
    min-width: 5rem;
}
</style>
