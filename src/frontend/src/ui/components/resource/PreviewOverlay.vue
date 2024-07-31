<script setup lang="ts">
import Button from "primevue/button";
import Portal from "primevue/portal";

const { header } = defineProps(["header"]);
const emit = defineEmits(["close"]);
</script>

<template>
    <Portal>
        <div @click="$emit('close')" class="z-50">
            <div class="fixed inset-0 bg-black bg-opacity-85 z-50"></div>

            <div class="fixed inset-0 flex justify-center items-center z-50 w-full flex-col h-full">
                <Button
                    @click="$emit('close')"
                    class="absolute right-5 top-2 opacity-50 hover:opacity-100"
                    size="large"
                    style="color: white"
                    icon="pi pi-times"
                    text
                ></Button>
                <div class="w-[80%] max-h-full flex flex-col divide-y divide-slate-800/25" @click="(e) => e.stopPropagation()">
                    <div v-if="!!header" :innerText="header" class="p-2 font-bold bg-gray-200 rounded-t-lg" />
                    <slot />
                </div>
            </div>
        </div>
    </Portal>
</template>
