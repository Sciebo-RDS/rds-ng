<script setup lang="ts">
import { onMounted, ref, watch } from "vue";

import { WebComponent } from "../../../component/WebComponent";
import { ComponentState, useComponentStore } from "../../../data/stores/ComponentStore";

import MessageDialog from "../../dialogs/MessageDialog.vue";

const comp = WebComponent.injectComponent();
const compStore = useComponentStore();

let activeState = ref(compStore.componentState);
watch(
    () => compStore.componentState,
    (state: ComponentState, prevState: ComponentState) => {
        activeState.value = state;
    }
);

onMounted(() => {
    compStore.queryParams = new URLSearchParams(window.location.search); // These might get lost, so store them
});
</script>

<template>
    <!-- Dialogs -->
    <ConfirmDialog :pt="{ icon: '!text-3xl', message: 'pt-1' }" group="confirm" />
    <ConfirmPopup :pt="{ icon: '!text-3xl', message: 'pt-1' }" group="confirmPopup" />
    <DynamicDialog />

    <MessageDialog />

    <!-- Notifications -->
    <Toast position="bottom-right" class="opacity-75" group="default" />
    <Toast
        position="bottom-center"
        class="opacity-75"
        group="status"
        :dt="{ width: 'auto', 'content.padding': '0.25rem', 'text.gap': '0' }"
        :pt="{ messageContent: 'items-center pl-2' }"
    >
        <template #message="slotProps">
            <div class="flex gap-1 mr-2">
                <span v-if="slotProps.message.icon" :class="slotProps.message.icon" /> <span>{{ slotProps.message.summary }}</span>
            </div>
        </template>
    </Toast>

    <!-- Main view -->
    <component :is="comp.userInterface.mainView.getStateComponent(activeState)"></component>
</template>
