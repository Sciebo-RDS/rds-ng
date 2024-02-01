<script setup lang="ts">
import { storeToRefs } from "pinia";
import { computed } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { FrontendSettingIDs } from "@/settings/FrontendSettingIDs";

import BasicLoginForm from "@/ui/misc/login/BasicLoginForm.vue";

const comp = FrontendComponent.inject();
const userStore = useUserStore();
const { userIDToken } = storeToRefs(userStore);

// If enabled, show the dummy login page to get a user ID token
const showLoginPage = computed(() => comp.data.config.value<boolean>(FrontendSettingIDs.UseLoginPage) && !userIDToken.value);
</script>

<template>
    <BasicLoginForm v-if="showLoginPage" />
    <RouterView v-else />
</template>

<style scoped lang="scss">

</style>
