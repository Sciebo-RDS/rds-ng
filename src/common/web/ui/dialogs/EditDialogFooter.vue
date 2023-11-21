<script setup lang="ts">
import Button from "primevue/button";

import { editDialogHandling } from "./EditDialogHandling";

const { acceptDialog, rejectDialog } = editDialogHandling();
</script>

<template>
    <!-- TODO: Customization -->
    <Button label="Save" icon="material-icons-outlined mi-done" size="small" @click="acceptDialog()"></Button>
    <Button label="Cancel" icon="material-icons-outlined mi-clear" size="small" @click="rejectDialog()"></Button>
</template>

<style scoped lang="scss">

</style>
