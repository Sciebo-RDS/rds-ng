<script setup lang="ts">
import { ref, inject } from "vue";
import { getRandomId } from "../utils/Ids";

import Checkbox from "primevue/checkbox";

import { PropertyController } from "../PropertyController";
import { PropertySet } from "../PropertySet";
import { type ProfileID } from "../PropertyProfile";

const props = defineProps(["property"]);

const controller = inject("controller") as PropertyController<PropertySet | PropertySet[]>;
const categoryId = inject("categoryId") as string;
const profileId = inject("profileId") as ProfileID;

const value = ref(controller.getValue(profileId, categoryId, props.property.id));

const handleInput = () => {
    controller.setValue(profileId, categoryId, props.property.id, value);
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
