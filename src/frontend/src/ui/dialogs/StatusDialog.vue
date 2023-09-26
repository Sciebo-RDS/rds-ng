<script setup lang="ts">
import { inject } from "vue";

const dialog = inject("dialogRef");
// @ts-ignore
const data = dialog.value.data;

const status = data.status;
const icon = data.icon;
</script>

<template>
    <div class="grid grid-flow-col items-center gap-3.5">
        <div v-if="icon !== ''" class="material-icons-outlined" style="font-size: 32px;">{{ icon }}</div>
        <div>{{ status }}</div>
    </div>
</template>

<style scoped lang="scss">

</style>
