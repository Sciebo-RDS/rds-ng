<script setup lang="ts">
import Button from "primevue/button";
import { inject } from "vue";

import { type EditDialogData } from "./EditDialog";

const dialogRef = inject("dialogRef") as any;
const dialogData = dialogRef.value.data as EditDialogData<any>;

function acceptDialog(): void {
    if (dialogData.accept) {
        dialogData.accept(dialogData.userData);
    }
    dialogRef.value.close(dialogData.userData);
}

function rejectDialog(): void {
    if (dialogData.reject) {
        dialogData.reject();
    }
    dialogRef.value.close();
}
</script>

<template>
    <!-- TODO: Customization -->
    <Button type="button" label="Save" icon="material-icons-outlined mi-done" size="small" @click="acceptDialog()"></Button>
    <Button type="button" label="Cancel" icon="material-icons-outlined mi-clear" size="small" @click="rejectDialog()"></Button>
</template>

<style scoped lang="scss">

</style>
