<script setup lang="ts">
import { storeToRefs } from "pinia";

import { useUserStore } from "@/data/stores/UserStore";
import PublishConnectionsListbox from "@/ui/dialogs/project/publish/PublishConnectionsListbox.vue";

const userStore = useUserStore();
const { userSettings } = storeToRefs(userStore);
</script>

<template>
    <div class="grid grid-rows-auto grid-flow-row grid-cols-[1fr] gap-1.5 w-full h-full">
        <div>To publish or export a project to a service, click on its corresponding button.</div>

        <PublishConnectionsListbox :user-settings="userSettings" />
    </div>
</template>

<style scoped lang="scss"></style>
