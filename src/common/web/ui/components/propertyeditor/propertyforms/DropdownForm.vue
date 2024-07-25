<script setup lang="ts">
import Dropdown from "primevue/dropdown";
import { computed, type PropType } from "vue";

import { ProjectObjectStore } from "../ProjectObjectStore";
import { type ProfileID } from "../PropertyProfile";

const props = defineProps({
    propertyObjectId: { type: String, required: true },
    inputId: { type: String, required: true },
    profileId: { type: Object as PropType<ProfileID[]>, required: false },
    projectObjects: { type: ProjectObjectStore, required: true },
    inputOptions: { type: Array as PropType<string[]>, required: true }
});

const value = computed(() => props.projectObjects.get(props.propertyObjectId)?.value as Record<string, any>);
</script>

<template>
    <div class="flex">
        <Dropdown
            :modelValue="value[inputId]"
            @update:modelValue="(value: String[]) => projectObjects.update(profileId || [], inputId, propertyObjectId, value)"
            :options="inputOptions"
            class="grow"
            placeholder="Select"
            filter
            :pt="{
                panel: {
                    class: 'w-0'
                }
            }"
        />
    </div>
</template>
