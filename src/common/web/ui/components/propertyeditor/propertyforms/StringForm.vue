<script setup lang="ts">
import { computed } from "vue";
import InputText from "primevue/inputtext";

import { ProjectObjectStore } from "../ProjectObjectStore";

const props = defineProps(["propertyObjectId", "inputId", "profileId", "projectObjects"]);

const value = computed(() => props.projectObjects.get(props.propertyObjectId).value);
</script>

<template>
    <div>
        <InputText
            type="text"
            :modelValue="value[inputId]"
            class="w-full"
            @input="(e) => projectObjects.update(profileId, inputId, 'string', propertyObjectId, e.target.value)"
        />
    </div>
</template>
