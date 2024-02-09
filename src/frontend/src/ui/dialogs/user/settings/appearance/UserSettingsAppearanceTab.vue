<script setup lang="ts">
import { type PropType, toRefs } from "vue";

import { UserSettings } from "@common/data/entities/user/UserSettings";

const props = defineProps({
    tabData: {
        type: Object as PropType<UserSettings>,
        required: true
    }
});
const propRefs = toRefs(props);
const userSettings = propRefs.tabData!;
</script>

<template>
    <div class="r-text-title">Appearance</div>
</template>

<style scoped lang="scss">

</style>
