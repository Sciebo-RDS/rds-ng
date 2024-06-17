<script setup lang="ts">
import { computed, type PropType } from "vue";
import { getRandomId } from "../utils/Ids";

import Button from "primevue/button";
import RadioButton from "primevue/radiobutton";

import { ProjectObjectStore } from "../ProjectObjectStore";
import { type ProfileID } from "../PropertyProfile";

const props = defineProps({
    propertyObjectId: { type: String, required: true },
    inputId: { type: String, required: true },
    profileId: { type: Object as PropType<ProfileID>, required: true },
    projectObjects: { type: ProjectObjectStore, required: true },
    inputOptions: { type: Array as PropType<string[]>, required: true }
});

const value = computed(() => props.projectObjects.get(props.propertyObjectId)?.value as Record<string, any>);

const id = getRandomId();
</script>

<template>
    <div class="card justify-content-center my-5">
        <div class="flex flex-col space-y-4">
            <div v-for="option in inputOptions" :key="option" class="flex align-items-center">
                <RadioButton
                    class="block"
                    :modelValue="value[inputId]"
                    :inputId="option + id"
                    name="dynamic"
                    :value="option"
                    @update:modelValue="(value: String) => projectObjects.update(profileId, inputId, propertyObjectId, value)"
                />
                <label :for="option + id" class="ml-2">{{ option }}</label>
            </div>
        </div>
        <div class="w-full grid">
            <Button
                @click="projectObjects.update(profileId, inputId, propertyObjectId, '')"
                icon="pi pi-times"
                severity="secondary"
                aria-label="clear selection"
                label="clear"
                class="justify-self-end"
                :class="!value[inputId] ? 'invisible' : ''"
                outlined
            />
        </div>
    </div>
</template>
