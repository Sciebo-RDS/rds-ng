<script setup lang="ts">
import Button from "primevue/button";

import { FrontendComponent } from "@/component/FrontendComponent";
import { projectActions } from "@/ui/actions/ProjectActions";

const comp = FrontendComponent.inject();
const emit = defineEmits(["projectCreated"]);
const { createProject } = projectActions(comp);
</script>

<template>
    <div class="place-self-stretch self-end m-4">
        <Button
            rounded
            class="w-full !p-1.5 !text-xl"
            label="New Project"
            icon="material-icons-outlined mi-add-circle-outline"
            icon-class="!text-4xl"
            @click="createProject((title, description) => emit('projectCreated', title, description))"
        />
    </div>
</template>

<style scoped lang="scss">

</style>
