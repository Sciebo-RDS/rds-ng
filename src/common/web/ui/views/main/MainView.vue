<script setup lang="ts">
import { ref, watch } from "vue";

import { WebComponent } from "../../../component/WebComponent";
import { ComponentState, componentStore } from "../../../data/stores/ComponentStore";

const comp = WebComponent.injectComponent();
const compStore = componentStore();

let activeState = ref(compStore.componentState);
watch(() => compStore.componentState, (state: ComponentState, prevState: ComponentState) => {
    activeState.value = state;
});
</script>

<template>
    <!-- Dialogs -->
    <ConfirmDialog />
    <ConfirmPopup />
    <DynamicDialog />

    <!-- Notifications -->
    <Toast position="bottom-right" class="opacity-75" />

    <!-- Main view -->
    <component :is="comp.userInterface.mainView.getStateComponent(activeState)"></component>
</template>
