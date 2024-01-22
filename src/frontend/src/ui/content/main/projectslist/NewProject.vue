<script setup lang="ts">
import { useProjectTools } from "@/ui/tools/ProjectTools";
import Button from "primevue/button";

import { FrontendComponent } from "@/component/FrontendComponent";

const comp = FrontendComponent.inject();
const { createProject } = useProjectTools(comp);
</script>

<template>
    <div class="place-self-stretch self-end m-4">
        <Button
            rounded
            class="w-full !p-1.5 !text-xl"
            label="New Project"
            icon="material-icons-outlined mi-add-circle-outline"
            icon-class="!text-4xl"
            @click="createProject"
        />
    </div>
</template>

<style scoped lang="scss">

</style>
