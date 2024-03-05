<script setup lang="ts">
import { useUrlSearchParams } from "@vueuse/core";
import { useAxios } from "@vueuse/integrations/useAxios";
import * as jwt from "jsonwebtoken";
import { storeToRefs } from "pinia";
import { computed, onMounted, unref, watch } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { FrontendSettingIDs } from "@/settings/FrontendSettingIDs";

import BasicLoginForm from "@/ui/misc/login/BasicLoginForm.vue";

const comp = FrontendComponent.inject();
const userStore = useUserStore();
const { userToken } = storeToRefs(userStore);

// If enabled, show the dummy login page to get a user ID token
const showLoginPage = computed(() => comp.data.config.value<boolean>(FrontendSettingIDs.UseLoginPage) && !userToken.value);

onMounted(() => {
    const pubKeyURL = comp.data.config.value<string>(FrontendSettingIDs.PublicKeyURL);
    console.log(pubKeyURL);

    const { data, isFinished } = useAxios(pubKeyURL);

    watch(isFinished, (f) => {
        if (f) {
            const key = JSON.parse(unref(data)["public-key"]);
            console.log(key);
            const queryParams = useUrlSearchParams("history");
            console.log(queryParams["user-token"]);
            jwt.verify(queryParams["user-token"], key);
        }
    });
});

</script>

<template>
    <BasicLoginForm v-if="showLoginPage" />
    <RouterView v-else />
</template>

<style scoped lang="scss">

</style>
