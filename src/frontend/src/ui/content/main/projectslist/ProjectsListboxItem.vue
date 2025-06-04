<script setup lang="ts">
import { storeToRefs } from "pinia";
import Button from "primevue/button";
import Menu from "primevue/menu";
import ProgressSpinner from "primevue/progressspinner";
import { computed, type PropType, ref, toRefs, unref } from "vue";

import { findConnectorInstanceByID } from "@common/data/entities/connector/ConnectorUtils";
import { Project } from "@common/data/entities/project/Project";

import { ConnectorCategory } from "@/data/entities/connector/categories/ConnectorCategory";
import { findConnectorCategoryByInstanceID } from "@/data/entities/connector/ConnectorUtils";
import { getAllProjectJobDetails } from "@/data/entities/project/ProjectJobUtils";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useProjectJobsStore } from "@/data/stores/ProjectJobsStore";
import { useProjectsStore } from "@/data/stores/ProjectsStore";
import { useUserStore } from "@/data/stores/UserStore";

import ProjectJobsCounterTag from "@/ui/components/project/ProjectJobsCounterTag.vue";

interface CountedCategory {
    category: ConnectorCategory;
    count: number;
    instances: Set<string>;
}

const consStore = useConnectorsStore();
const { connectors } = storeToRefs(consStore);
const userStore = useUserStore();
const { userSettings } = storeToRefs(userStore);
const projStore = useProjectsStore();
const { projects } = storeToRefs(projStore);
const projJobsStore = useProjectJobsStore();
const { jobs } = storeToRefs(projJobsStore);
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
const { project, isSelected, isDeleted } = toRefs(props);
const emits = defineEmits<{
    (e: "upload-project", project: Project): void;
    (e: "edit-project", project: Project): void;
    (e: "delete-project", project: Project): void;
}>();

const runningJobs = computed(() =>
    getAllProjectJobDetails(unref(projects), unref(jobs), unref(connectors), unref(userSettings).connector_instances).filter(
        (details) => details.job.project_id == unref(project)!.project_id
    )
);

const finishedJobCategories = computed(() => {
    const categories: CountedCategory[] = [];
    unref(project)!.logbook.job_history.forEach((record) => {
        if (!record.success) {
            return;
        }

        const category = findConnectorCategoryByInstanceID(unref(connectors), unref(userSettings).connector_instances, record.connector_instance);
        if (category) {
            let counter = categories.find((cat: CountedCategory) => cat.category == category);
            if (!counter) {
                counter = { category: category, count: 0, instances: new Set<string>() } as CountedCategory;
                categories.push(counter);
            }
            counter.count += 1;

            const connectorInstance = findConnectorInstanceByID(unref(userSettings).connector_instances, record.connector_instance);
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
                label: "Upload project",
                icon: "material-icons-outlined mi-rocket-launch",
                command: () => {
                    emits("upload-project", project!.value);
                }
            },
            {
                label: "Project settings",
                icon: "material-icons-outlined mi-settings",
                command: () => {
                    emits("edit-project", project!.value);
                }
            },
            { separator: true },
            {
                label: "Delete project",
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
    <div
        class="p-2 pl-3 grid grid-rows-[auto_auto_1fr] grid-cols-[1fr_min-content] grid-flow-row w-full gap-0 min-h-24 content-start items-start place-content-start group r-text border-l-4"
        :class="{ 'border-[var(--p-rds-highlight-500)]': isSelected, 'border-transparent': !isSelected }"
    >
        <div class="r-text-caption-big h-7 truncate" :title="project!.title">{{ project!.title }}</div>

        <div v-if="!isDeleted" class="row-span-2 pl-1">
            <Button
                text
                rounded
                size="small"
                aria-label="Options"
                title="More options"
                :class="{ invisible: !editMenuShown, 'group-hover:visible': true }"
                @click.stop="(event) => editMenu.toggle(event)"
            >
                <template #icon>
                    <span class="material-icons-outlined mi-more-vert r-text" style="font-size: 32px" />
                </template>
            </Button>
            <Menu ref="editMenu" :model="editMenuItems" popup @focus="editMenuShown = true" @blur="editMenuShown = false" />
        </div>
        <div v-else class="row-span-2 pl-1">
            <ProgressSpinner class="w-8 h-8" strokeWidth="4" />
        </div>

        <div v-if="!isDeleted" id="project-description" class="overflow-hidden line-clamp-2" :title="project.description">
            {{ project!.description }}
        </div>
        <div v-else class="italic">The project is currently being deleted...</div>

        <div class="grid grid-cols-[1fr_min-content] self-end col-span-2 r-text-gray">
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

<style></style>
