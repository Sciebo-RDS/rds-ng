<script setup lang="ts">
import DatePicker from "primevue/datepicker";
import { computed } from "vue";

import { PropertyObjectStore } from "../PropertyObjectStore";

const props = defineProps({
    propertyObjectId: { type: String, required: true },
    inputId: { type: String, required: true },
    propertyObjects: { type: PropertyObjectStore, required: true }
});

const value = computed(() => props.propertyObjects.get(props.propertyObjectId)?.getValues() as Record<string, any>);
</script>

<template>
    <div>
        <DatePicker
            @date-select="(date: Date) => propertyObjects.update(inputId, propertyObjectId, date)"
            update-model-type="string"
            dateFormat="dd/mm/yy"
            v-model="value[inputId]"
            class="w-full"
        />
    </div>
</template>
