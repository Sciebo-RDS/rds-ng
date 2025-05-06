<script setup lang="ts">
import { computed, type PropType } from "vue";
import { getRandomId } from "../utils/Ids";

import Checkbox from "primevue/checkbox";

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
    <div class="grid grid-cols-2 gap-4 place-content-stretch">
        <div v-for="option of inputOptions" :key="option">
            <Checkbox
                :modelValue="value[inputId]"
                :inputId="option + id"
                :name="option"
                :value="option"
                class="mr-2"
                @update:modelValue="(val: String[]) => propertyObjects.update(inputId, propertyObjectId, val)"
            />
            <label class="break-all" :for="option + id">{{ option }}</label>
        </div>
    </div>
</template>
