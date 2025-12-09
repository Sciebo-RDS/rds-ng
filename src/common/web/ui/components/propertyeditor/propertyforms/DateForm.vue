<script setup lang="ts">
import DatePicker from "primevue/datepicker";
import { computed } from "vue";

import { PropertyObjectStore } from "../PropertyObjectStore";

const props = defineProps({
    propertyObjectId: { type: String, required: true },
    inputId: { type: String, required: true },
    propertyObjects: { type: PropertyObjectStore, required: true }
});

const value = computed(() => {
    const values = props.propertyObjects.get(props.propertyObjectId)?.getValues();
    try {
        if (!!values && !!values[props.inputId]) {
            return new Date(values[props.inputId]);
        }
    } catch (e) {}
    return undefined;
});
</script>

<template>
    <div>
        <DatePicker
            v-model="value"
            update-model-type="date"
            date-format="yy-mm-dd"
            @date-select="(date: Date) => propertyObjects.update(props.inputId, props.propertyObjectId, date)"
            fluid
        />
    </div>
</template>
