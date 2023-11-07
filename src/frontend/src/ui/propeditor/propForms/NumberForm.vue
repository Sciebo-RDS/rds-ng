<script setup lang="ts">
import { ref, inject } from "vue";
import InputNumber from "primevue/inputnumber";

const props = defineProps(["property"]);

const controller = inject("controller");
const categoryId = inject("categoryId");

// TODO: Handle overflows
let value = ref(controller.getValue(categoryId, props.property.id));

let debounce: number | null = null;

let handleInput = (e: Event) => {
    debounce = controller.setValue(
        debounce,
        categoryId,
        props.property.id,
        e.value
    );
};
</script>

<template>
    <div class="">
        <InputNumber
            @input="handleInput"
            v-model="value"
            :useGrouping="false"
            class="w-full"
        />
    </div>
</template>
