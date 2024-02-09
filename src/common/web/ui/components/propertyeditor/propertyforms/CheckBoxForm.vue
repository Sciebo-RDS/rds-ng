<script setup lang="ts">
import { ref, inject } from "vue";
import { getRandomId } from "../utils/Ids.ts";

import Checkbox from "primevue/checkbox";

import { PropertyController } from "@common/ui/components/propertyeditor/PropertyController";

const props = defineProps(["property"]);

const controller: PropertyController = inject("controller");
const categoryId = inject("categoryId");
const profileId = inject("profileId");

const value = ref(controller.getValue(profileId, categoryId, props.property.id));

// BUG the debounce only works for the first checked box, might be a library bug or some js quirks
let debounce: number | null = null;

const handleInput = () => {
    debounce = controller.setValue(profileId, debounce, categoryId, props.property.id, value);
};

const id = getRandomId();
</script>

<template>
    <div class="grid grid-cols-2 gap-4 place-content-stretch">
        <div v-for="option of property.options" :key="option">
            <Checkbox v-model="value" :inputId="option + id" :name="option" :value="option" @change="handleInput" class="mr-2" />
            <label class="break-all" :for="option + id">{{ option }}</label>
        </div>
    </div>
</template>
../utils/Ids.js
