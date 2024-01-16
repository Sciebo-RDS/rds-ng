<script setup lang="ts">
import { toRefs } from "vue";

import { UserSettings } from "@common/data/entities/user/UserSettings";

const props = defineProps({
    tabData: {
        required: true
    }
});
const propRefs = toRefs(props);
const userSettings = propRefs.tabData as UserSettings;
</script>

<template>
    <div>Appearance here!</div>
</template>

<style scoped lang="scss">

</style>
