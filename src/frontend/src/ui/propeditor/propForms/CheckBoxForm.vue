<script setup lang="ts">
import { ref, inject } from "vue";
import Checkbox from "primevue/checkbox";

const props = defineProps(["property"]);

const controller = inject("controller");
const categoryId = inject("categoryId");

let value = ref(controller.getValue(categoryId, props.property.id));

let debounce: number | null = null;

let handleInput = (e: string) => {
    console.log(value);
    debounce = controller.setValue(
        debounce,
        categoryId,
        props.property.id,
        value
    );
};
</script>

<template>
    <div class="grid grid-cols-2 gap-4 place-content-stretch">
        <div v-for="option of property.options" :key="option">
            <Checkbox
                v-model="value"
                :inputId="option"
                name="option"
                :value="option"
                @change="handleInput"
                class="mr-2"
            />
            <label class="break-all" :for="option">{{ option }}</label>
        </div>
    </div>
</template>
