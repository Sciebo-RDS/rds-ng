<script setup lang="ts">
import { storeToRefs } from "pinia";
import { computed } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { LoginType } from "@/integration/Login";
import { FrontendSettingIDs } from "@/settings/FrontendSettingIDs";

import BasicLogin from "@/ui/misc/login/BasicLogin.vue";
import HostLogin from "@/ui/misc/login/HostLogin.vue";

const comp = FrontendComponent.inject();
const userStore = useUserStore();
const { userToken } = storeToRefs(userStore);

const loginForms = {
    [LoginType.Basic]: BasicLogin,
    [LoginType.Host]: HostLogin
};

const loginType = comp.data.config.value<LoginType>(FrontendSettingIDs.LoginType);
const isLoggedIn = computed(() => !!userToken.value);
</script>

<template>
    <RouterView v-if="isLoggedIn" />
    <component v-else :is="loginForms[loginType]" />
</template>

<style scoped lang="scss">

</style>
