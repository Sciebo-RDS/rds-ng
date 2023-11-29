<script setup lang="ts">
import Button from "primevue/button";
import { ref, watch } from "vue";

import { extendedDialogTools } from "./ExtendedDialogTools";

const { acceptDialog, rejectDialog, dialogData } = extendedDialogTools();

const errors = ref([]);
// We need this "double watch", as the validator doesn't necessarily exist (yet)
watch(
    () => dialogData.validator,
    (validator) => {
        if (validator) {
            watch(
                () => validator.errors,
                (err) => {
                    errors.value = err ? Object.values(err) : [];
                }
            );
        }
    }
);
</script>

<template>
    <div
        class="grid grid-rows-1 grid-cols-[1fr_min-content_min-content] items-center !pt-[1.5rem] shadow-inner"
    >
        <small v-if="errors.length" class="p-error mr-auto text-left">
            <span class="font-bold"
                >One or more fields in the form are missing or invalid:</span
            >
            <br />
            <span class="italic">
                {{ errors[0] }}
                <span v-if="errors.length > 1"
                    >(+ {{ errors.length - 1 }} more)</span
                >
            </span>
        </small>
        <small v-else>&nbsp;</small>
        <Button
            v-if="dialogData.options.hasAcceptButton"
            :label="dialogData.options.acceptLabel || 'OK'"
            :icon="dialogData.options.acceptIcon"
            size="small"
            :disabled="false"
            @click="acceptDialog"
            class="!ml-2 !mr-0"
        />
        <Button
            v-if="dialogData.options.hasRejectButton"
            :label="dialogData.options.rejectLabel || 'Cancel'"
            :icon="dialogData.options.rejectIcon"
            size="small"
            @click="rejectDialog"
            class="!ml-2 !mr-0"
        />
    </div>
</template>

<style scoped lang="scss"></style>
