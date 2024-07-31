<script setup lang="ts">
import Button from "primevue/button";
import { ref, watch } from "vue";

import { useExtendedDialogTools } from "@common/ui/dialogs/ExtendedDialogTools";

import ErrorsMessage from "@common/ui/components/misc/ErrorsMessage.vue";

defineProps({
    prevName: {
        type: String,
        default: "Back"
    },
    prevIcon: {
        type: String,
        default: "mi-arrow-back"
    },
    prevIconPosition: {
        type: true,
        default: "left"
    },
    prevCallback: {
        type: true
    },
    nextName: {
        type: String,
        default: "Next"
    },
    nextCallback: {
        type: true
    },
    nextIcon: {
        type: String,
        default: "mi-arrow-forward"
    },
    nextIconPosition: {
        type: true,
        default: "right"
    }
});
const { dialogData } = useExtendedDialogTools();

const errors = ref([]);
if (!!dialogData.validator) {
    watch(
        () => dialogData.validator!.errors,
        (err) => {
            errors.value = err ? Object.values(err) : [];
        }
    );
}
</script>

<template>
    <div class="grid grid-cols-[max-content_1fr_max-content]">
        <Button
            v-if="!!prevCallback"
            :label="prevName"
            severity="secondary"
            :icon="'material-icons-outlined ' + prevIcon"
            :icon-pos="prevIconPosition"
            size="small"
            class="button-width"
            @click="prevCallback"
        />
        <div v-else class="button-width" />

        <small v-if="errors.length" class="p-error text-center">
            <ErrorsMessage :errors="errors" />
        </small>
        <small v-else>&nbsp;</small>

        <Button
            :label="nextName"
            :icon="'material-icons-outlined ' + nextIcon"
            :icon-pos="nextIconPosition"
            size="small"
            class="button-width"
            :disabled="!nextCallback"
            @click="nextCallback"
        />
    </div>
</template>

<style scoped lang="scss">
.button-width {
    @apply min-w-24;
}
</style>
