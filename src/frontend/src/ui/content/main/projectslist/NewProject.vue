<script setup lang="ts">
import Button from "primevue/button";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useProjectTools } from "@/ui/tools/project/ProjectTools";

const comp = FrontendComponent.inject();
const { newProject } = useProjectTools(comp);
</script>

<template>
    <div class="p-2">
        <Button
            severity=""
            class="w-full h-full text-xl grid grid-flow-col place-content-center text-[var(--p-primary-100)]"
            label="New project"
            icon="material-icons-outlined mi-add-circle-outline"
            icon-class="!text-4xl mr-2"
            @click="newProject"
            :pt="{ label: 'mr-auto' }"
        />
    </div>
</template>

<style scoped lang="scss"></style>
