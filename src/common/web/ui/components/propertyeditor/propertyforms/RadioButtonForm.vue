<script setup lang="ts">
import { computed, inject } from "vue";
import { getRandomId } from "../utils/Ids";

import RadioButton from "primevue/radiobutton";
import Button from "primevue/button";

import { PropertyController } from "../PropertyController";
import { PropertySet } from "../PropertySet";
import { type ProfileID } from "../PropertyProfile";

const props = defineProps(["property"]);

const controller = inject("controller") as PropertyController<PropertySet | PropertySet[]>;
const categoryId = inject("categoryId") as string;
const profileId = inject("profileId") as ProfileID;

const value = computed(() => controller.getValue(profileId, categoryId, props.property.id));

const handleInput = (eValue: Event) => {
    controller.setValue(profileId, categoryId, props.property.id, eValue);
};

const id = getRandomId();
</script>

<template>
    <div class="card flex justify-content-center">
        <Button
            @click="
                value = null;
                handleInput(value as Event);
            "
            icon="pi pi-times"
            severity="secondary"
            text
            rounded
            aria-label="unset"
            class="m-0 p-0 mr-5 max-h-4 max-w-[1.65rem]"
        />
        <div class="flex flex-column gap-3">
            <div v-for="option in property.options" :key="option" class="flex align-items-center">
                <RadioButton :modelValue="value" :inputId="option + id" name="dynamic" :value="option" @update:modelValue="handleInput" />
                <label :for="option + id" class="ml-2">{{ option }}</label>
            </div>
        </div>
    </div>
</template>
../utils/Ids.js
