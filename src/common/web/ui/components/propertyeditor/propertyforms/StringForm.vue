<script setup lang="ts">
import InputText from "primevue/inputtext";
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
        <InputText type="text" v-model="value[inputId]" class="w-full" @update:modelValue="(val) => propertyObjects.update(inputId, propertyObjectId, val)" />
    </div>
</template>
