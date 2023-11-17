<script setup lang="ts">
import { ref, inject } from "vue";
import Chips from "primevue/chips";

const props = defineProps(["property"]);

const controller = inject("controller");
const categoryId = inject("categoryId");
const profileId = inject("profileId");

const value = ref(
    controller.getValue(profileId, categoryId, props.property.id)
);

let debounce: number | null = null;

const handleInput = (eValue: Event) => {
    debounce = controller.setValue(
        profileId,
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
        :placeholder="!value || value.length === 0 ? 'Separate by comma' : null"
    />
</template>
