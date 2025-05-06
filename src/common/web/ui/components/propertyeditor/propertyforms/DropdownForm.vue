<script setup lang="ts">
import Select from "primevue/select";
import { computed, type PropType } from "vue";

import { PropertyObjectStore } from "../PropertyObjectStore";

const props = defineProps({
    propertyObjectId: { type: String, required: true },
    inputId: { type: String, required: true },
    propertyObjects: { type: PropertyObjectStore, required: true },
    inputOptions: { type: Array as PropType<string[]>, required: true }
});

const value = computed(() => props.propertyObjects.get(props.propertyObjectId)?.getValues() as Record<string, any>);
</script>

<template>
    <div class="flex">
        <Select
            :modelValue="value[inputId]"
            @update:modelValue="(value: String[]) => propertyObjects.update(inputId, propertyObjectId, value)"
            filter-placeholder="Search entry"
            :options="inputOptions"
            class="grow"
            placeholder="Select"
            filter
            :pt="{ overlay: 'w-0' }"
        />
    </div>
</template>
