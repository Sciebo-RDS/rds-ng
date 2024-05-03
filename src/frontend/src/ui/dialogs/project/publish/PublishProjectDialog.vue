<script setup lang="ts">
import { storeToRefs } from "pinia";
import { ref, unref, watch } from "vue";

import { Project } from "@common/data/entities/project/Project";
import { useExtendedDialogTools } from "@common/ui/dialogs/ExtendedDialogTools";

import { useProjectsStore } from "@/data/stores/ProjectsStore";
import { useUserStore } from "@/data/stores/UserStore";

import PublishConnectionsListbox from "@/ui/dialogs/project/publish/PublishConnectionsListbox.vue";

const { dialogData } = useExtendedDialogTools();

const project = ref<Project>(dialogData.userData.project);
const userStore = useUserStore();
const projStore = useProjectsStore();
const { userSettings } = storeToRefs(userStore);

// Projects will be updated if a job is completed, so we need to react accordingly
watch(
    () => projStore.projects,
    (projects: Project[]) => {
        // Since all jobs are updated, we need to "re-find" our current one and use the new instance
        const id = unref(project)!.project_id;
        const projectUpd = projects.find((proj) => proj.project_id == id);
        if (projectUpd) {
            project.value = projectUpd;
        }
    },
);
</script>

<template>
    <div class="grid grid-rows-auto grid-flow-row grid-cols-[1fr] gap-1.5 w-full h-full">
        <div>To publish or export a project to a service, click on its corresponding button.</div>

        <PublishConnectionsListbox :project="project" :user-settings="userSettings" />
    </div>
</template>

<style scoped lang="scss"></style>
