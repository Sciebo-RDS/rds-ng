<script setup lang="ts">
import { storeToRefs } from "pinia";
import BlockUI from "primevue/blockui";
import Message from "primevue/message";
import { toRefs } from "vue";

import { useFrontendStore } from "@/data/stores/FrontendStore";

const frontendStore = useFrontendStore();
const props = defineProps({
    initializing: {
        type: Boolean,
        required: true,
    },
});
const { initializationMessage, initializationError } = storeToRefs(frontendStore);
const { initializing } = toRefs(props);
</script>

<template>
    <BlockUI :blocked="initializing" full-screen />
    <Message v-if="initializing" :severity="initializationError ? 'error' : 'info'" class="overlay-message" :closable="false"
        >{{ initializationMessage }}
    </Message>
</template>

<style scoped lang="scss">
.overlay-message {
    @apply absolute top-1/2 left-1/2 z-[9999] #{!important};
    transform: translate(-50%, -50%);
}
</style>
