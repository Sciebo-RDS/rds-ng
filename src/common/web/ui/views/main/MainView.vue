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
    },
);

onMounted(() => {
    compStore.queryParams = new URLSearchParams(window.location.search); // These might get lost, so store them
});
</script>

<template>
    <!-- Dialogs -->
    <ConfirmDialog />
    <ConfirmPopup />
    <DynamicDialog />

    <MessageDialog />

    <!-- Notifications -->
    <Toast position="bottom-right" class="opacity-75" />

    <!-- Main view -->
    <component :is="comp.userInterface.mainView.getStateComponent(activeState)"></component>
</template>
