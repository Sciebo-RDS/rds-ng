<script setup lang="ts">
import Button from "primevue/button";

import { extendedDialogTools } from "./ExtendedDialogTools";

const { acceptDialog, rejectDialog, dialogData } = extendedDialogTools();
</script>

<template>
    <Button v-if="dialogData.options.hasAcceptButton" :label="dialogData.options.acceptLabel || 'OK'" :icon="dialogData.options.acceptIcon" size="small" @click="acceptDialog" />
    <Button v-if="dialogData.options.hasRejectButton" :label="dialogData.options.rejectLabel || 'Cancel'" :icon="dialogData.options.rejectIcon" size="small" @click="rejectDialog" />
</template>

<style scoped lang="scss">

</style>
