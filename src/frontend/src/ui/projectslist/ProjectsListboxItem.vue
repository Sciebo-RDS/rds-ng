<script setup lang="ts">
import { ref, toRefs } from "vue";
import Button from "primevue/button";
import Menu from "primevue/menu";

import { FrontendComponent } from "@/component/FrontendComponent";
import { DeleteProjectAction } from "@/ui/actions/DeleteProjectAction";
import { confirmDeleteProjectDialog } from "@/dialogs/ConfirmDeleteProjectDialog";

const comp = FrontendComponent.inject();

const props = defineProps(['project', 'isSelected']);
const state = toRefs(props);
const project = state.project;
const isSelected = state.isSelected;

const editMenu = ref();
const editMenuItems = ref([
    {
        label: "Edit project",
        items: [
            {
                label: "Edit project",
                icon: "material-icons-outlined mi-edit",
                command: () => {
                }
            },
            { separator: true },
            {
                label: "Delete project",
                icon: "material-icons-outlined mi-delete-forever",
                class: "r-text-error",
                command: () => {
                    const dialog = confirmDeleteProjectDialog(comp, props.project);
                    dialog.then(() => {
                        const action = new DeleteProjectAction(comp);
                        action.prepare(props.project);
                        action.execute();
                    });
                }
            }
        ]
    }
]);
const editMenuShown = ref(false);
</script>

<template>
    <div class="grid grid-rows-[auto_auto] grid-cols-[1fr_min-content] gap-0 h-24 place-content-start group">
        <div class="r-text-caption-big h-8 truncate" :title="project.name">{{ project.name }}</div>
        <div class="row-span-2 pl-1">
            <Button text rounded size="small" aria-label="Options" title="More options" :class="{ 'invisible': !editMenuShown, 'group-hover:visible': true }" @click="event => editMenu.toggle(event)">
                <template #icon>
                    <span class="material-icons-outlined mi-more-vert" :class="[isSelected ? 'r-primary-text' : 'r-text']" style="font-size: 32px;"/>
                </template>
            </Button>
            <Menu ref="editMenu" :model="editMenuItems" popup @focus="editMenuShown=true" @blur="editMenuShown=false"/>
        </div>

        <div id="project-description" class="overflow-hidden line-clamp" :title="project.description">{{ project.description }}</div>
    </div>
</template>

<style scoped lang="scss">
#project-description {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}
</style>
