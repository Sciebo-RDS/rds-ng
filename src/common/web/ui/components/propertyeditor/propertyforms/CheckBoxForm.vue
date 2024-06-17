<script setup lang="ts">
import { computed, type PropType } from "vue";
import { getRandomId } from "../utils/Ids";

import Checkbox from "primevue/checkbox";

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
    <div class="grid grid-cols-2 gap-4 place-content-stretch">
        <div v-for="option of inputOptions" :key="option">
            <Checkbox
                :modelValue="value[inputId]"
                :inputId="option + id"
                :name="option"
                :value="option"
                class="mr-2"
                @update:modelValue="(value: String[]) => projectObjects.update(profileId, inputId, propertyObjectId, value)"
            />
            <label class="break-all" :for="option + id">{{ option }}</label>
        </div>
    </div>
</template>
