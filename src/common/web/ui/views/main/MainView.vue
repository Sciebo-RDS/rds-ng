<script setup lang="ts">
import { ref, watch } from "vue";
import { WebComponent } from "../../../component/WebComponent";

import { ComponentState, componentStore } from "../../../stores/ComponentStore";
import ConnectionErrorView from "./landing/ConnectionErrorView.vue";
import ConnectionLostView from "./landing/ConnectionLostView.vue";
import InitializingView from "./landing/InitializingView.vue";

const comp = WebComponent.inject();
const compStore = componentStore();
const views = {
    "InitializingView": InitializingView,
    "ConnectionLostView": ConnectionLostView,
    "ConnectionErrorView": ConnectionErrorView,
    "RunningView": comp.appRoot,
};

function componentStateToView(state: ComponentState): number {
    switch (state) {
        case ComponentState.Initializing:
            return "InitializingView";

        case ComponentState.Running:
            return "RunningView";

        case ComponentState.ConnectionLost:
            return "ConnectionLostView";

        case ComponentState.ConnectionError:
            return "ConnectionErrorView";
    }
    return "";
}

let activeView = ref(componentStateToView(compStore.componentState));
watch(() => compStore.componentState, (state: ComponentState, prevState: ComponentState) => {
    activeView.value = componentStateToView(state);
});
</script>

<template>
    <component :is="views[activeView]"></component>
</template>
