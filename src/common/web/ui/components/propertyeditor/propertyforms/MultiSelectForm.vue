<script setup lang="ts">
import { computed, type PropType } from "vue";
import MultiSelect from "primevue/multiselect";

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
</script>

<template>
    <div>
        <MultiSelect
            v-model="value[inputId]"
            :options="inputOptions"
            class="w-full relative"
            @update:modelValue="(value: String[]) => projectObjects.update(profileId, inputId, 'multiselect', propertyObjectId, value)"
        />
    </div>
</template>
