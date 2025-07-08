<script setup lang="ts">
import Button from "primevue/button";
import { toRefs } from "vue";

import { Project } from "@common/data/entities/project/Project";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useProjectTools } from "@/ui/tools/project/ProjectTools";

const comp = FrontendComponent.inject();
const props = defineProps({
    project: {
        type: Project,
        required: true
    }
});
const { project } = toRefs(props);
const { editProject, uploadProject } = useProjectTools(comp);
</script>

<template>
    <div class="flex gap-2">
        <Button
            label="Project settings"
            icon="material-icons-outlined mi-edit-note text-[var(--p-primary-100)]"
            icon-class="!text-3xl"
            @click="editProject(project)"
            :pt="{ label: 'text-[var(--p-primary-100)]' }"
            rounded
        />
        <Button
            severity="contrast"
            label="Upload project"
            icon="material-icons-outlined mi-rocket-launch"
            icon-class="!text-3xl"
            class="px-8 mr-0"
            @click="uploadProject(project)"
            rounded
        />
    </div>
</template>

<style scoped lang="scss"></style>
