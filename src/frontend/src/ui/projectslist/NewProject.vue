<script setup lang="ts">
import Button from "primevue/button";

import { FrontendComponent } from "@/component/FrontendComponent";
import { CreateProjectAction } from "@/ui/actions/CreateProjectAction";

const comp = FrontendComponent.inject();
const emit = defineEmits(["projectCreated"]);

function createNewProject() {
    // TODO: Dialog
    const title = "I have no title";
    const description = "And also no description :(";

    const action = new CreateProjectAction(comp);
    action.prepare(title, description);
    action.execute();

    emit("projectCreated", title, description);
}
</script>

<template>
    <div class="place-self-stretch self-end m-4">
        <Button
            rounded
            class="w-full !p-2 !text-xl"
            label="New Project"
            icon="material-icons-outlined mi-add-circle-outline"
            icon-class="!text-4xl"
            @click="createNewProject"
        />
    </div>
</template>

<style scoped lang="scss"></style>
