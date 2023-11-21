<script setup lang="ts">
import Button from "primevue/button";

import { useEditDialogHandling } from "./EditDialogHandling";

const { acceptDialog, rejectDialog, dialogData } = useEditDialogHandling();
</script>

<template>
    <Button :label="dialogData.options.acceptLabel || 'OK'" :icon="dialogData.options.acceptIcon || 'material-icons-outlined mi-done'" size="small" @click="acceptDialog()" />
    <Button :label="dialogData.options.rejectLabel || 'Cancel'" :icon="dialogData.options.rejectIcon || 'material-icons-outlined mi-clear'" size="small" @click="rejectDialog()" />
</template>

<style scoped lang="scss">

</style>
