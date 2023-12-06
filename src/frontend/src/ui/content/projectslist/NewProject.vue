<script setup lang="ts">
import Button from "primevue/button";

import { FrontendComponent } from "@/component/FrontendComponent";
import { CreateProjectAction } from "@/ui/actions/CreateProjectAction";

const comp = FrontendComponent.inject();

function createProject() {
    const action = new CreateProjectAction(comp);
    action.showEditDialog().then((data) => {
        action.prepare(data.title, data.description, data.selectedFeatures);
        action.execute();
    });
}
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
