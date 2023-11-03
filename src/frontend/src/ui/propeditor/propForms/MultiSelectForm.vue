<script setup lang="ts">
import { ref, inject } from "vue";
import MultiSelect from "primevue/multiselect";

const props = defineProps(["property"]);

const controller = inject("controller");
const categoryId = inject("categoryId");

let value = ref(controller.getValue(categoryId, props.property.id));

let debounce: number | null = null;

function handleInput(e: Event) {
    if (debounce) {
        clearTimeout(debounce);
    }
    debounce = setTimeout(() => {
        controller.setValue(categoryId, props.property.id, e.value);
    }, 500);
}
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
