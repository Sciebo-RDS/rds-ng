<script setup lang="ts">
import { ref } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";

import { extendedDialogTools } from "@common/ui/dialogs/ExtendedDialogTools";

import type { UserSettings } from "@common/data/entities/user/UserSettings";

const { dialogData } = extendedDialogTools();

const comp = FrontendComponent.inject();
const userSettings = ref<UserSettings>(dialogData.userData.settings);
</script>

<template>
    <div>Ok I am pretty empty...</div>
</template>

<style scoped lang="scss">

</style>
