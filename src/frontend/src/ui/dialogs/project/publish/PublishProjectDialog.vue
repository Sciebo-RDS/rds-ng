<script setup lang="ts">
import { storeToRefs } from "pinia";
import { ref } from "vue";

import { Project } from "@common/data/entities/project/Project";
import { useExtendedDialogTools } from "@common/ui/dialogs/ExtendedDialogTools";

import { useUserStore } from "@/data/stores/UserStore";

import PublishConnectionsListbox from "@/ui/dialogs/project/publish/PublishConnectionsListbox.vue";

const { dialogData } = useExtendedDialogTools();

const project = ref<Project>(dialogData.userData.project);
const userStore = useUserStore();
const { userSettings } = storeToRefs(userStore);
</script>

<template>
    <div class="grid grid-rows-auto grid-flow-row grid-cols-[1fr] gap-1.5 w-full h-full">
        <div class="mb-2">To publish or export a project to a service, click on its corresponding button.</div>

        <PublishConnectionsListbox :project="project" :user-settings="userSettings" />
    </div>
</template>

<style scoped lang="scss"></style>
