<script setup lang="ts">
// @ts-nocheck
import { storeToRefs } from "pinia";
import Listbox from "primevue/listbox";
import ScrollPanel from "primevue/scrollpanel";
import { watch } from "vue";
import { useRoute } from "vue-router";

import { Project, type ProjectID, ProjectStatus } from "@common/data/entities/project/Project";

import { FrontendComponent } from "@/component/FrontendComponent";
import { DisplayState, useFrontendStore } from "@/data/stores/FrontendStore.ts";
import { useProjectsStore } from "@/data/stores/ProjectsStore";
import { TouchProjectAction } from "@/ui/actions/project/TouchProjectAction.ts";
import { useProjectTools } from "@/ui/tools/project/ProjectTools";

import ProjectsListboxItem from "@/ui/content/main/projectslist/ProjectsListboxItem.vue";

const comp = FrontendComponent.inject();
const route = useRoute();
const frontendStore = useFrontendStore();
const projStore = useProjectsStore();

const { displayState } = storeToRefs(frontendStore);
const { projects, activeProject } = storeToRefs(projStore);
const { uploadProject, editProject, deleteProject } = useProjectTools(comp);

const unwatchProjects = watch(projects, () => {
    // If the current URL contains a project ID, select that project once we received our projects list
    if (route.params.hasOwnProperty("project_id")) {
        let projectID = route.params.project_id as string;
        selectProject(parseInt(projectID), true);
    }

    unwatchProjects();
});

watch(
    activeProject,
    (newProj, oldProj) => {
        // Prevent deselecting the currently selected project item
        if (newProj === null && !!oldProj) {
            activeProject.value = oldProj;
        }

        if (activeProject.value !== oldProj) {
            // Notify the server about the project being selected
            if (!!activeProject.value) {
                const action = new TouchProjectAction(comp, true);
                action.prepare(activeProject.value);
                action.execute();
            }

            // Switch the display mode only if a project is selected
            if (activeProject.value) {
                displayState.value = DisplayState.Project;
            }

            // Update the shown URL to reflect the selected project
            comp.userInterface.frontendView.navigateTo(true, undefined, { project_id: activeProject.value });
        }
    },
    { flush: "post" }
);

function selectProject(projectID: ProjectID | undefined, autoNavigateOnMissing: boolean = false): void {
    if (!projects.value.find((proj) => proj.project_id === projectID)) {
        projectID = undefined;

        if (autoNavigateOnMissing) {
            displayState.value = DisplayState.Landing;
            comp.userInterface.frontendView.navigateTo(true);
        }
    }
    activeProject.value = projectID;
}

function isProjectSelected(project: Project): boolean {
    return project.project_id === activeProject.value;
}

function isProjectDeleted(project: Project): boolean {
    return project.status == ProjectStatus.Deleted || projStore.pendingDeletions.includes(project.project_id);
}
</script>

<template>
    <ScrollPanel class="h-full">
        <Listbox
            v-model="activeProject"
            :options="projects"
            option-value="project_id"
            :option-disabled="isProjectDeleted"
            class="w-full h-fit"
            :pt="{
                root: 'projects-listbox',
                listContainer: 'projects-listbox-container',
                list: 'projects-listbox-list',
                option: 'projects-listbox-option'
            }"
            :dt="{ 'option.selected.background': 'var(--p-surface-50)', 'option.selected.focus.background': 'var(--p-surface-50)' }"
        >
            <template #option="projectEntry">
                <ProjectsListboxItem
                    :project="projectEntry.option"
                    :is-selected="isProjectSelected(projectEntry.option)"
                    :is-deleted="isProjectDeleted(projectEntry.option)"
                    @dblclick="editProject(projectEntry.option)"
                    @upload-project="uploadProject(projectEntry.option)"
                    @edit-project="editProject(projectEntry.option)"
                    @delete-project="deleteProject(projectEntry.option)"
                />
            </template>
            <template #empty>
                <div class="r-text-caption-big r-small-caps grid justify-center">No current projects</div>
            </template>
        </Listbox>
    </ScrollPanel>
</template>

<style scoped lang="scss">
:deep(.projects-listbox) {
    // Max height is 100% - header height (5rem) - footer height (6rem)
    // did not work out, need 1 less rem because of wonky behaviour when overlay panel is active
    @apply border-0 rounded-none bg-surface-50 max-h-[calc(100vh-5rem-7rem)] #{!important};
}

:deep(.projects-listbox-container) {
    @apply max-h-full #{!important};
}

:deep(.projects-listbox-list) {
    @apply p-0 gap-0 #{!important};
}

:deep(.projects-listbox-option) {
    @apply m-0.5 mb-0 p-0 border-0 rounded-none #{!important};
}
</style>
