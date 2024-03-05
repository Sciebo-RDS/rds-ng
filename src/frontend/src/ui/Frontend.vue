<script setup lang="ts">
import { storeToRefs } from "pinia";
import { computed, onMounted } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { useHostIntegration } from "@/integration/HostIntegration";
import { FrontendSettingIDs } from "@/settings/FrontendSettingIDs";

import BasicLoginForm from "@/ui/misc/login/BasicLoginForm.vue";

const comp = FrontendComponent.inject();
const userStore = useUserStore();
const { userToken } = storeToRefs(userStore);

// If enabled, show the dummy login page to get a user ID token
const showLoginPage = computed(() => comp.data.config.value<boolean>(FrontendSettingIDs.UseLoginPage) && !userToken.value);

onMounted(() => {
    const { getUserToken } = useHostIntegration(comp);
    getUserToken().then((userToken) => {
        console.log(userToken);
    }).catch((error) => {
        console.log(error);
    });
});

</script>

<template>
    <BasicLoginForm v-if="showLoginPage" />
    <RouterView v-else />
</template>

<style scoped lang="scss">

</style>
