<script setup lang="ts">
import { computed } from "vue";
import { HintType, propertyDataForms, PropertyDataType } from "../PropertyProfile";
import InputHints from "./InputHints.vue";

const { propertyClass, propertyObject, propertyObjects, isDialog, input } = defineProps([
    "propertyClass",
    "propertyObject",
    "propertyObjects",
    "isDialog",
    "input"
]);

// checks if there are hints available for the current input
const hasHints = computed(() => input.hasHints(propertyObject.getValues()[input.getId()]));
</script>

<template>
    <div>
        <span v-if="input.getLabel() !== propertyClass.getDisplayLabel()" :class="{ 'font-bold': isDialog }">
            {{ input.getLabel() }}
        </span>
        <div v-if="isDialog && input.getLabel() !== propertyClass.getDisplayLabel()" class="r-text-gray">
            {{ input.getDescription() }}
        </div>

        <div v-if="isDialog && input.getExample()" v-html="`Example: ${input.getExample()}`" />
        <component
            :is="propertyDataForms[input.getType() as PropertyDataType]"
            class="w-full"
            :propertyObjectId="propertyObject.getId()"
            :propertyObjects="propertyObjects"
            :inputId="input.getId()"
            :inputOptions="input.getOptions()"
        />
        <InputHints
            v-if="hasHints"
            :hint-link="input.getHint(propertyObject.getValues()[input.getId()], HintType.Link)"
            :hint-text="input.getHint(propertyObject.getValues()[input.getId()], HintType.Text)"
        />
    </div>
</template>
