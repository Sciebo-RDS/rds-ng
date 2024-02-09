<script setup lang="ts">
import Button from "primevue/button";
import Menu from "primevue/menu";
import ProgressSpinner from "primevue/progressspinner";
import { type PropType, ref, toRefs } from "vue";

import { Project } from "@common/data/entities/project/Project";

import { FrontendComponent } from "@/component/FrontendComponent";

const comp = FrontendComponent.inject();
const props = defineProps({
    project: {
        type: Object as PropType<Project>,
        required: true
    },
    isSelected: {
        type: Boolean,
        default: false
    },
    isDeleted: {
        type: Boolean,
        default: false
    }
});
const emits = defineEmits<{
    (e: "edit-project", project: Project): void;
    (e: "delete-project", project: Project): void;
}>();

const { project, isSelected, isDeleted } = toRefs(props);

const editMenu = ref();
const editMenuItems = ref([
    {
        label: "Edit project",
        items: [
            {
                label: "Settings",
                icon: "material-icons-outlined mi-engineering",
                command: () => {
                    emits("edit-project", project!.value);
                }
            },
            { separator: true },
            {
                label: "Delete",
                icon: "material-icons-outlined mi-delete-forever",
                class: "r-text-error",
                command: () => {
                    emits("delete-project", project!.value);
                }
            }
        ]
    }
]);
const editMenuShown = ref(false);
</script>

<template>
    <div class="grid grid-rows-[auto_auto] grid-cols-[1fr_min-content] grid-flow-row gap-0 h-24 place-content-start group">
        <div class="r-text-caption-big h-8 truncate" :title="project!.title">{{ project!.title }}</div>

        <div v-if="!isDeleted" class="row-span-2 pl-1">
            <Button
                text
                rounded
                size="small"
                aria-label="Options"
                title="More options"
                :class="{ invisible: !editMenuShown, 'group-hover:visible': true }"
                @click="(event) => editMenu.toggle(event)"
            >
                <template #icon>
                    <span class="material-icons-outlined mi-more-vert" :class="[isSelected ? 'r-highlight-text' : 'r-text']" style="font-size: 32px" />
                </template>
            </Button>
            <Menu ref="editMenu" :model="editMenuItems" popup @focus="editMenuShown = true" @blur="editMenuShown = false" />
        </div>
        <div v-else class="row-span-2 pl-1">
            <ProgressSpinner class="w-8 h-8" strokeWidth="4" />
        </div>

        <div v-if="!isDeleted" id="project-description" class="overflow-hidden line-clamp" :title="project.description">{{ project!.description }}</div>
        <div v-else class="italic">The project is currently being deleted...</div>
    </div>
</template>

<style scoped lang="scss">
#project-description {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}
</style>
