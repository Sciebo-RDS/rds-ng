<script setup lang="ts">
import { storeToRefs } from "pinia";
import Card from "primevue/card";
import ScrollPanel from "primevue/scrollpanel";
import { ref } from "vue";

import { Project } from "@common/data/entities/project/Project";
import { useExtendedDialogTools } from "@common/ui/dialogs/ExtendedDialogTools";

import { useUserStore } from "@/data/stores/UserStore";

import UploadConnectionsList from "@/ui/dialogs/project/upload/UploadConnectionsList.vue";

const { dialogData } = useExtendedDialogTools();

const project = ref<Project>(dialogData.userData.project);
const userStore = useUserStore();
const { userSettings } = storeToRefs(userStore);
</script>

<template>
    <div class="grid grid-rows-[min-content_1fr] gap-1.5 w-full h-full">
        <div v-if="userSettings.connector_instances.length > 0" class="mb-2">
            To upload your project to an external service, click on its corresponding button.
        </div>
        <Card v-else class="bg-amber-100 text-amber-700 !p-0 mt-4 w-full" :pt="{ title: '!text-base', caption: 'h-5', body: 'p-3 px-5' }">
            <template #title>
                <div class="flex items-center gap-1">
                    <span class="material-icons-outlined mi-warning-amber !text-xl" />
                    <span class="">No connections added</span>
                </div>
            </template>
            <template #content>
                <span class="text-sm">
                    You haven't added any connections to external services yet. To be able to upload your project, go to your settings
                    <span class="material-icons-outlined mi-settings relative top-1.5" /> and add at least one connection to an external service.
                </span>
            </template>
        </Card>

        <ScrollPanel v-if="userSettings.connector_instances.length > 0" class="h-[46rem] min-h-[32rem]">
            <UploadConnectionsList :project="project" :user-settings="userSettings" />
        </ScrollPanel>
    </div>
</template>

<style scoped lang="scss"></style>
