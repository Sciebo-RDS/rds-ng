<script setup lang="ts">
import { ref, inject } from "vue";
import Dropdown from "primevue/dropdown";

const props = defineProps(["property"]);

const controller = inject("controller");
const categoryId = inject("categoryId");
const profileId = inject("profileId");

const value = ref(
    controller.getValue(profileId, categoryId, props.property.id)
);

let debounce: number | null = null;

const handleInput = (e: string) => {
    console.log(e.value);
    debounce = controller.setValue(
        profileId,
        debounce,
        categoryId,
        props.property.id,
        e.value
    );
};
</script>

<template>
    <div class="flex">
        <Dropdown
            v-model="value"
            @change="handleInput"
            :options="property.options"
            class="grow"
            placeholder="Select"
            filter
            :pt="{
                panel: {
                    class: 'w-0',
                },
            }"
        />
    </div>
</template>
