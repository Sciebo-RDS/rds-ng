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
    <div class="r-text-title">Appearance</div>
</template>

<style scoped lang="scss">

</style>
