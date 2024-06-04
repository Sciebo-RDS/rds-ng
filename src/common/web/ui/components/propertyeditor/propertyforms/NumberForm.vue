<script setup lang="ts">
import { computed, type PropType } from "vue";
import InputNumber from "primevue/inputnumber";
import { type InputNumberInputEvent } from "primevue/inputnumber";

import { ProjectObjectStore } from "../ProjectObjectStore";
import { type ProfileID } from "../PropertyProfile";

const props = defineProps({
    propertyObjectId: { type: String, required: true },
    inputId: { type: String, required: true },
    profileId: { type: Object as PropType<ProfileID>, required: true },
    projectObjects: { type: ProjectObjectStore, required: true }
});

const value = computed(() => props.projectObjects.get(props.propertyObjectId)?.value as Record<string, any>);
</script>

<template>
    <div>
        <!-- 
            @update:modelValue on InputNumber is weird: https://github.com/primefaces/primevue/issues/506
         -->
        <InputNumber
            v-model="value[inputId]"
            :useGrouping="false"
            class="w-full"
            @input="(e: InputNumberInputEvent) => projectObjects.update(profileId, inputId, 'number', propertyObjectId, e.value)"
        />
    </div>
</template>
