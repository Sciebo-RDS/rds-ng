<script setup lang="ts">
import Button from "primevue/button";
import Menu from "primevue/menu";
import ProgressSpinner from "primevue/progressspinner";
import { computed, type PropType, ref, toRefs, unref } from "vue";

import { findConnectorInstanceByID } from "@common/data/entities/connector/ConnectorUtils";
import { Project } from "@common/data/entities/project/Project";

import { ConnectorCategory } from "@/data/entities/connector/categories/ConnectorCategory";
import { findConnectorCategoryByInstanceID } from "@/data/entities/connector/ConnectorUtils";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useProjectJobsStore } from "@/data/stores/ProjectJobsStore";
import { getAllProjectJobDetails } from "@/data/entities/project/ProjectJobUtils";
import { useProjectsStore } from "@/data/stores/ProjectsStore";
import { useUserStore } from "@/data/stores/UserStore";

import ProjectJobsCounterTag from "@/ui/components/project/ProjectJobsCounterTag.vue";

interface CountedCategory {
    category: ConnectorCategory;
    count: number;
    instances: Set<string>;
}

const consStore = useConnectorsStore();
const userStore = useUserStore();
const projStore = useProjectsStore();
const projJobsStore = useProjectJobsStore();
const props = defineProps({
    project: {
        type: Object as PropType<Project>,
        required: true,
    },
    isSelected: {
        type: Boolean,
        default: false,
    },
    isDeleted: {
        type: Boolean,
        default: false,
    },
});
const { project, isSelected, isDeleted } = toRefs(props);
const emits = defineEmits<{
    (e: "edit-project", project: Project): void;
    (e: "delete-project", project: Project): void;
}>();

const runningJobs = computed(() =>
    getAllProjectJobDetails(projStore.projects, projJobsStore.jobs, consStore.connectors, userStore.userSettings.connector_instances).filter(
        (details) => details.job.project_id == unref(project)!.project_id,
    ),
);

const finishedJobCategories = computed(() => {
    const categories: CountedCategory[] = [];
    unref(project)!.logbook.job_history.forEach((record) => {
        if (!record.success) {
            return;
        }

        const category = findConnectorCategoryByInstanceID(consStore.connectors, userStore.userSettings.connector_instances, record.connector_instance);
        if (category) {
            let counter = categories.find((cat: CountedCategory) => cat.category == category);
            if (!counter) {
                counter = { category: category, count: 0, instances: new Set<string>() } as CountedCategory;
                categories.push(counter);
            }
            counter.count += 1;

            const connectorInstance = findConnectorInstanceByID(userStore.userSettings.connector_instances, record.connector_instance);
            if (connectorInstance) {
                counter.instances.add(connectorInstance.name);
            }
        }
    });
    categories.sort((a, b) => a.category.name.localeCompare(b.category.name));
    return categories;
});

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
                },
            },
            { separator: true },
            {
                label: "Delete",
                icon: "material-icons-outlined mi-delete-forever",
                class: "r-text-error",
                command: () => {
                    emits("delete-project", project!.value);
                },
            },
        ],
    },
]);
const editMenuShown = ref(false);
</script>

<template>
    <div class="grid grid-rows-[auto_auto_1fr] grid-cols-[1fr_min-content] grid-flow-row gap-0 min-h-24 content-start items-start place-content-start group">
        <div class="r-text-caption-big h-7 truncate" :title="project!.title">{{ project!.title }}</div>

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

        <div class="grid grid-cols-[1fr_min-content] self-end text-slate-600 col-span-2">
            <span v-if="runningJobs.length > 0" class="grid grid-cols-[min-content_auto] items-center text-sm">
                <span class="material-icons-outlined mi-rocket-launch mr-1 !text-lg" />
                <span class="pt-0.5">
                    {{ [...new Set(runningJobs.map((details) => details.connectorCategory?.verbStatusProgressing || "Exporting"))].join(", ") }}...
                </span>
            </span>
            <span v-else />

            <span>
                <span v-for="category in finishedJobCategories" class="pl-1.5">
                    <ProjectJobsCounterTag :value="category.count" :category="category.category" :instance-names="[...category.instances]" />
                </span>
            </span>
        </div>
    </div>
</template>

<style scoped lang="scss">
#project-description {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}
</style>
