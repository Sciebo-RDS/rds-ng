<script setup lang="ts">
import { ref, inject } from "vue";
import RadioButton from "primevue/radiobutton";
import Button from "primevue/button";

const props = defineProps(["property"]);

const controller = inject("controller");
const categoryId = inject("categoryId");
const profileId = inject("profileId");

let value = ref(controller.getValue(profileId, categoryId, props.property.id));

let debounce: number | null = null;

let handleInput = (eValue: Event) => {
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
    <div class="card flex justify-content-center">
        <Button
            @click="
                value = null;
                handleInput(value);
            "
            icon="pi pi-times"
            severity="secondary"
            text
            rounded
            aria-label="unset"
            class="m-0 p-0 mr-5 max-h-4 max-w-[1.65rem]"
        />
        <div class="flex flex-column gap-3">
            <div
                v-for="option in property.options"
                :key="option"
                class="flex align-items-center"
            >
                <RadioButton
                    v-model="value"
                    :inputId="option"
                    name="dynamic"
                    :value="option"
                    @update:modelValue="handleInput"
                />
                <label :for="option" class="ml-2">{{ option }}</label>
            </div>
        </div>
    </div>
</template>
