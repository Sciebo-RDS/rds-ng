<script setup lang="ts">
import { ref, inject } from "vue";
import Chips from "primevue/chips";

const props = defineProps(["property"]);

const controller = inject("controller");
const categoryId = inject("categoryId");

let value = ref(controller.getValue(categoryId, props.property.id));

let debounce: number | null = null;

let handleInput = (eValue: Event) => {
    debounce = controller.setValue(
        debounce,
        categoryId,
        props.property.id,
        eValue
    );
};
</script>

<template>
    <Chips
        @update:modelValue="handleInput"
        v-model="value"
        separator=","
        class="inline"
        :addOnBlur="true"
        placeholder="Separate by comma"
    />
</template>
