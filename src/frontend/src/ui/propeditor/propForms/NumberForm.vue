<script setup lang="ts">
import { ref } from "vue";
import InputNumber from "primevue/inputnumber";

const props = defineProps(["property", "category_name", "controller"]);

let value = ref(
    props.controller.getValue(props.category_name, props.property.name)
);

let debounce: number | null = null;

function handleInput(e: any) {
    if (debounce) {
        clearTimeout(debounce);
    }
    console.log(typeof e);
    debounce = setTimeout(() => {
        props.controller.setValue(
            props.category_name,
            props.property.name,
            e.value
        );
        console.log(props.controller.propertiesToString());
    }, 500);
}
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
