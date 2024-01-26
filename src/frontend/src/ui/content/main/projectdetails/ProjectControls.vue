<script setup lang="ts">
import Button from "primevue/button";
import { toRefs } from "vue";

import { Project } from "@common/data/entities/project/Project";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useProjectTools } from "@/ui/tools/ProjectTools";

const comp = FrontendComponent.inject();
const props = defineProps({
    project: {
        type: Project,
        required: true
    }
});
const { project } = toRefs(props);
const { editProject } = useProjectTools(comp);
</script>

<template>
    <div>
        <Button
            severity="secondary"
            label="Project settings"
            icon="material-icons-outlined mi-engineering"
            icon-class="!text-3xl"
            @click="editProject(project)"
        />
    </div>
</template>

<style scoped lang="scss">

</style>
