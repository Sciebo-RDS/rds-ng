<script setup lang="ts">
import BlockUI from "primevue/blockui";
import Message from "primevue/message";
import { toRefs } from "vue";

const props = defineProps({
    initializing: {
        type: Boolean,
        required: true,
    },
    message: {
        type: String,
        required: true,
    },
    isError: {
        type: Boolean,
        default: false,
    },
});
const { initializing, message, isError } = toRefs(props);
</script>

<template>
    <BlockUI :blocked="initializing" full-screen />
    <Message v-if="initializing" :severity="isError ? 'error' : 'info'" class="overlay-message" :closable="false">{{ message }}</Message>
</template>

<style scoped lang="scss">
.overlay-message {
    @apply absolute top-1/2 left-1/2 z-[9999] #{!important};
    transform: translate(-50%, -50%);
}
</style>
