<script setup lang="ts">
import Button from "primevue/button";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useProjectTools } from "@/ui/tools/project/ProjectTools";

const comp = FrontendComponent.inject();
const { newProject } = useProjectTools(comp);
</script>

<template>
    <div class="place-self-stretch self-end m-4">
        <Button
            class="w-full !p-1.5 !text-xl"
            label="New Project"
            icon="material-icons-outlined mi-add-circle-outline"
            icon-class="!text-4xl"
            severity="warning"
            @click="newProject"
        />
    </div>
</template>

<style scoped lang="scss"></style>
