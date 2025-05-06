<script setup lang="ts">
import { ref } from "vue";

import Button from "primevue/button";
import Popover from "primevue/popover";

const props = defineProps(["propertyClass", "index"]);
const emit = defineEmits(["remove"]);

const showRemovePropertyPopover = ref();

const togglePopover = (e: Event) => {
    showRemovePropertyPopover.value.toggle(e);
};
</script>

<template>
    <div>
        <div class="text-gray-400 mt-0 pt-0 text-lg ml-auto mr-2" :class="props.propertyClass.isRequired() ? '' : 'group-hover:hidden'">{{ props.index }}.</div>

        <Popover ref="showRemovePropertyPopover" class="py-2 px-5">
            <div class="flex flex-col gap-4">
                <h3 class="text-lg font-bold">Remove "{{ props.propertyClass.getDisplayLabel() }}"?</h3>
                <p>The data for property "{{ props.propertyClass.getDisplayLabel() }}" will be lost. Linked Property Objects will be preserved.</p>
                <div class="flex gap-2 ml-auto">
                    <Button severity="danger" @click="emit('remove', props.propertyClass.getId())"> Delete </Button>
                    <Button outlined @click="togglePopover($event)">Cancel </Button>
                </div>
            </div>
        </Popover>

        <Button
            :disabled="props.propertyClass.isRequired()"
            text
            icon="pi pi-trash"
            :aria-label="'Remove ' + props.propertyClass.getDisplayLabel()"
            :title="'Remove ' + props.propertyClass.getDisplayLabel()"
            :class="props.propertyClass.isRequired() ? 'invisible' : 'invisible group-hover:visible'"
            class="pt-0 mt-0 h-9"
            @click="togglePopover($event)"
            :pt="{ root: 'text-gray-400 hover:text-red-600 bg-transparent' }"
        />
    </div>
</template>
