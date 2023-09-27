<script setup lang="ts">
import DynamicDialog from "primevue/dynamicdialog";
import Toast from "primevue/toast";
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
    <DynamicDialog></DynamicDialog>
    <Toast></Toast>
    <component :is="comp.mainView.getStateComponent(activeState)"></component>
</template>
