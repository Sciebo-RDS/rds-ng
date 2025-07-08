<script setup lang="ts">
import { storeToRefs } from "pinia";
import Button from "primevue/button";
import OverlayBadge from "primevue/overlaybadge";
import Popover from "primevue/popover";
import { computed, ref, unref } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { getUnseenProjectJobHistoryRecords } from "@/data/entities/project/ProjectUtils";
import { DisplayState, useFrontendStore } from "@/data/stores/FrontendStore.ts";
import { useProjectJobsStore } from "@/data/stores/ProjectJobsStore";
import { useProjectsStore } from "@/data/stores/ProjectsStore";
import { useUserStore } from "@/data/stores/UserStore";

import ProjectJobsPanel from "@/ui/content/main/jobspanel/ProjectJobsPanel.vue";
import { UserSettingsPage } from "@/ui/dialogs/user/settings/UserSettingsDialog.ts";
import { useUserTools } from "@/ui/tools/user/UserTools";

const comp = FrontendComponent.inject();
const frontendStore = useFrontendStore();
const projStore = useProjectsStore();
const projJobsStore = useProjectJobsStore();
const userStore = useUserStore();

const { displayState } = storeToRefs(frontendStore);
const { projects, activeProject } = storeToRefs(projStore);
const { jobs } = storeToRefs(projJobsStore);
const { userSettings } = storeToRefs(userStore);
const { editUserSettings } = useUserTools(comp);

const jobsPanel = ref();
const jobsPanelIcon = computed(() => (unref(jobs).length ? "material-icons-outlined mi-notifications-active" : "material-icons-outlined mi-notifications"));
const jobPanelBadgeCounter = computed(() => {
    let count: number = unref(jobs).length;
    count += unref(projects)
        .map((project) => getUnseenProjectJobHistoryRecords(project).length)
        .reduce((v, acc) => v + acc, 0);
    return count;
});

function onGoHome(): void {
    displayState.value = DisplayState.Landing;
    activeProject.value = undefined;
    comp.userInterface.frontendView.navigateTo(true, undefined, { project_id: undefined });
}

function onShowJobsPanel(event: Event): void {
    unref(jobsPanel).toggle(event);
}

function onHelp(): void {
    editUserSettings(userSettings.value, UserSettingsPage.Support);
}

function onEditUserSettings(): void {
    editUserSettings(userSettings.value);
}
</script>

<template>
    <div
        class="grid grid-cols-[min-content_1fr_max-content] grid-flow-col gap-y-3 content-center items-center r-primary-bg r-primary-text border-r-2 border-[var(--p-primary-200)]"
    >
        <div>
            <a href="#" @click.prevent="onGoHome">
                <img id="logo" src="@assets/img/logo-bridgit-inv.svg" alt="RDS Logo" class="p-4 pl-1 min-w-56" title="Home" />
            </a>
        </div>

        <div class="flex gap-x-1 pr-2 ml-auto">
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
                    class="inset-[-0.5rem] pt-px"
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

            <Button
                plain
                rounded
                aria-label="Help"
                title="Help"
                icon="material-icons-outlined mi-help-outline"
                icon-class="r-primary-text !text-4xl"
                class="size-12"
                @click="onHelp"
            />
        </div>

        <Popover ref="jobsPanel">
            <ProjectJobsPanel :projects="projects" :jobs="jobs" />
        </Popover>
    </div>
</template>

<style scoped lang="scss"></style>
