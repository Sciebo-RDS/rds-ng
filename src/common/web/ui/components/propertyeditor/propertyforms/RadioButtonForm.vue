<script setup lang="ts">
import { computed, type PropType } from "vue";
import { getRandomId } from "../utils/Ids";

import RadioButton from "primevue/radiobutton";

import { PropertyObjectStore } from "../PropertyObjectStore";

const props = defineProps({
    propertyObjectId: { type: String, required: true },
    inputId: { type: String, required: true },
    propertyObjects: { type: PropertyObjectStore, required: true },
    inputOptions: { type: Array as PropType<string[]>, required: true }
});

const value = computed(() => props.propertyObjects.get(props.propertyObjectId)?.getValues() as Record<string, any>);

const id = getRandomId();
</script>

<template>
    <div v-if="!!inputOptions" class="justify-content-center items-center">
        <div class="flex flex-wrap gap-4">
            <span v-for="option in inputOptions" :key="option" class="flex shrink grow-0 items-start">
                <RadioButton
                    class="block"
                    :modelValue="value[inputId]"
                    :inputId="option + id"
                    name="dynamic"
                    :value="option"
                    @update:modelValue="(val: String) => propertyObjects.update(inputId, propertyObjectId, val)"
                />
                <label :for="option + id" class="ml-2 break-all leading-snug">{{ option }}</label>
            </span>

            <span class="flex shrink grow-0 items-start">
                <RadioButton
                    class="block"
                    :inputId="`reset` + propertyObjectId"
                    name="dynamic"
                    @click="propertyObjects.update(inputId, propertyObjectId, '')"
                />
                <label :for="`reset` + propertyObjectId" class="ml-2 break-all leading-snug">none</label>
            </span>
        </div>
    </div>
</template>
