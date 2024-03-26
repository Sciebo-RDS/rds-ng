<script setup lang="ts">
import { useProjectsStore } from "@/data/stores/ProjectsStore";
import { useUserTools } from "@/ui/tools/UserTools";
import { storeToRefs } from "pinia";
import Button from "primevue/button";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";

const comp = FrontendComponent.inject();
const projStore = useProjectsStore();
const userStore = useUserStore();
const { projects } = storeToRefs(projStore);
const { userToken, userSettings } = storeToRefs(userStore);
const { editUserSettings } = useUserTools(comp);

function onEditUserSettings(): void {
    editUserSettings(userSettings.value);
}
</script>

<template>
    <div class="grid grid-rows-2 grid-cols-[min-content_1fr_min-content] grid-flow-col gap-x-2 content-center items-center r-primary-bg r-primary-text">
        <div class="row-span-2">
            <a href="https://www.research-data-services.org" target="_blank">
                <img id="logo" src="@assets/img/rds-octopus-wh.svg" alt="RDS Logo" class="p-1.5" title="Visit the RDS website" />
            </a>
        </div>

        <div class="font-bold self-center pt-3">
            <div v-if="userToken" :title="userToken.user_id">{{ userToken.user_name }}</div>
            <div v-else>(No user logged in)</div>
        </div>

        <div class="italic self-center pb-3">
            <div v-if="projects.length > 1">{{ projects.length }} projects</div>
            <div v-else-if="projects.length == 1">{{ projects.length }} project</div>
            <div v-else>No projects</div>
        </div>
        <div class="row-span-2 pr-2">
            <Button plain rounded aria-label="Settings" title="Settings" @click="onEditUserSettings">
                <template #icon>
                    <span class="material-icons-outlined mi-settings r-primary-text" style="font-size: 40px" />
                </template>
            </Button>
        </div>
    </div>
</template>

<style scoped lang="scss">
#logo {
    min-width: 5rem;
}
</style>
