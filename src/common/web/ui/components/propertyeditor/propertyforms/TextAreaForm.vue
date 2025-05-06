<script setup lang="ts">
import Textarea from "primevue/textarea";
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
        <Textarea @update:modelValue="(val) => propertyObjects.update(inputId, propertyObjectId, val)" v-model="value[inputId]" autoResize class="w-full" />
    </div>
</template>
