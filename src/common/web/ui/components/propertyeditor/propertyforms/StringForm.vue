<script setup lang="ts">
import InputText from "primevue/inputtext";
import { computed, type PropType } from "vue";
import { ProjectObjectStore } from "../ProjectObjectStore";
import { type ProfileID } from "../PropertyProfile";

const props = defineProps({
    propertyObjectId: { type: String, required: true },
    inputId: { type: String, required: true },
    profileId: { type: Object as PropType<ProfileID>, required: true },
    projectObjects: { type: ProjectObjectStore, required: true },
    globalObjectStore: {
        type: Object as PropType<ProjectObjectStore>,
        required: true
    }
});

const value = computed(() => props.projectObjects.get(props.propertyObjectId)?.value as Record<string, any>);
</script>

<template>
    <div>
        <InputText
            type="text"
            v-model="value[inputId]"
            class="w-full"
            @update:modelValue="(value) => projectObjects.update(profileId, inputId, propertyObjectId, value)"
        />
    </div>
</template>
