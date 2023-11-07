<script setup lang="ts">
import { ref, inject } from "vue";
import MultiSelect from "primevue/multiselect";

const props = defineProps(["property"]);

const controller = inject("controller");
const categoryId = inject("categoryId");

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
        <MultiSelect
            @change="handleInput"
            v-model="value"
            :options="property.options"
            class="w-full"
        />
    </div>
</template>
