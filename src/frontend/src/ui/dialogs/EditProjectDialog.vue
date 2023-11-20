<script setup lang="ts">
import InputText from "primevue/inputtext";
import Textarea from "primevue/textarea";
import { inject } from "vue";

import { type EditDialogData } from "@common/ui/dialogs/EditDialog";

import { FrontendComponent } from "@/component/FrontendComponent";
import { type EditProjectDialogData } from "@/ui/dialogs/EditProjectDialog";

const dialogRef = inject("dialogRef") as any;
const dialogData = dialogRef.value.data as EditDialogData<EditProjectDialogData>;

const comp = FrontendComponent.inject();
</script>

<template>
    <!-- TODO: Make pretty <3 -->
    <div class="grid grid-rows-auto grid-cols-[min-content_1fr] gap-5">
        <label>Title</label>
        <InputText v-model="dialogData.userData.title" placeholder="Title" />

        <label>Description</label>
        <Textarea v-model="dialogData.userData.description" placeholder="Description" rows="3" />
    </div>
</template>

<style scoped lang="scss">

</style>
