<script setup lang="ts">
import InputNumber, { type InputNumberInputEvent } from "primevue/inputnumber";
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
        <!-- 
            @update:modelValue on InputNumber is weird: https://github.com/primefaces/primevue/issues/506
         -->
        <InputNumber
            v-model="value[inputId]"
            :useGrouping="false"
            class="w-full"
            @input="(e: InputNumberInputEvent) => propertyObjects.update(inputId, propertyObjectId, e.value)"
        />
    </div>
</template>
