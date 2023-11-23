<script setup lang="ts">
import Button from "primevue/button";

import MandatoryMark from "../forms/MandatoryMark.vue";

import { extendedDialogTools } from "./ExtendedDialogTools";

const { acceptDialog, rejectDialog, dialogData } = extendedDialogTools();
</script>

<template>
    <div class="grid grid-rows-1 grid-cols-[1fr_min-content_min-content] place-items-baseline">
        <small v-if="dialogData.options.showMandatoryHint" class="p-error italic">
            <MandatoryMark />
            denotes mandatory fields</small>
        <small v-else>&nbsp;</small>
        <Button v-if="dialogData.options.hasAcceptButton" :label="dialogData.options.acceptLabel || 'OK'" :icon="dialogData.options.acceptIcon" size="small" @click="acceptDialog" />
        <Button v-if="dialogData.options.hasRejectButton" :label="dialogData.options.rejectLabel || 'Cancel'" :icon="dialogData.options.rejectIcon" size="small" @click="rejectDialog" />
    </div>
</template>

<style scoped lang="scss">

</style>
