<script setup lang="ts">
import Button from "primevue/button";

import { Dialog } from "@common/ui/dialogs/Dialog";

const dialog = Dialog.inject();
</script>

<template>
    <Button label="OK" @click="dialog?.close()" autofocus rounded/>
</template>

<style scoped lang="scss">

</style>
