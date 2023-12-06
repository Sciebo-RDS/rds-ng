<script setup lang="ts">
import { onMounted } from "vue";

import { WebComponent } from "../../../component/WebComponent";

const comp = WebComponent.injectComponent();

// Always run our web component when the main Vue component has been mounted
onMounted(() => {
    comp.run();
});
</script>

<template>
    <router-view />
</template>
