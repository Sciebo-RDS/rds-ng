<script setup lang="ts">
import { ref } from "vue";
import MultiSelect from "primevue/multiselect";

const props = defineProps(["property", "category_name", "controller"]);

let value = ref(
    props.controller.getValue(props.category_name, props.property.name)
);

let debounce: number | null = null;

function handleInput(e: any) {
    if (debounce) {
        clearTimeout(debounce);
    }
    debounce = setTimeout(() => {
        props.controller.setValue(
            props.category_name,
            props.property.name,
            e.value
        );
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
