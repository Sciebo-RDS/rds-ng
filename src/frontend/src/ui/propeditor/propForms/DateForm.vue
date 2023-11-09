<script setup lang="ts">
import { ref, inject } from "vue";
import Calendar from "primevue/calendar";

const props = defineProps(["property"]);

const controller = inject("controller");
const categoryId = inject("categoryId");

let value = ref(controller.getValue(categoryId, props.property.id));

let debounce: number | null = null;

let handleInput = (eValue: string) => {
    let ms: number = new Date(eValue).getTime();
    console.log(ms);
    debounce = controller.setValue(debounce, categoryId, props.property.id, ms);
};
</script>

<template>
    <div class="">
        <Calendar
            @update:modelValue="handleInput"
            dateFormat="yy/mm/dd"
            v-model="value"
            class="w-full"
            view="year"
        />
    </div>
</template>
