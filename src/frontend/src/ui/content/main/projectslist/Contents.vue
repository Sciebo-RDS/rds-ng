<script setup lang="ts">
import { storeToRefs } from "pinia";
import Card from "primevue/card";

import LinkedText from "@common/ui/components/misc/LinkedText.vue";

import { FrontendComponent } from "@/component/FrontendComponent.ts";
import { useUserStore } from "@/data/stores/UserStore.ts";

import NewProject from "@/ui/content/main/projectslist/NewProject.vue";
import ProjectsListbox from "@/ui/content/main/projectslist/ProjectsListbox.vue";
import { useUserTools } from "@/ui/tools/user/UserTools.ts";

const comp = FrontendComponent.inject();
const userStore = useUserStore();

const { editUserSettings } = useUserTools(comp);
const { userSettings } = storeToRefs(userStore);
</script>

<template>
    <div class="grid grid-rows-[min-content_1fr_4.25rem] grid-cols-1 bg-surface-50 border-r border-[var(--p-surface-200)]">
        <Card
            v-if="userSettings.connector_instances.length == 0"
            class="bg-amber-100 text-amber-700 rounded-none mx-0.5 mt-0.5 !p-0 shadow-none"
            :pt="{ title: '!text-base', body: 'p-1.5 px-2.5 text-pretty' }"
        >
            <template #title>
                <div class="flex items-center gap-1">
                    <span class="material-icons-outlined mi-link-off !text-xl" />
                    <span class="">No connections added</span>
                </div>
            </template>
            <template #content>
                <span class="text-sm">
                    To enter metadata for your projects and to upload them, you need to add connections to external services in your
                    <LinkedText text="settings" @click="() => editUserSettings(userSettings)" icon-class="material-icons-outlined mi-settings" />.
                </span>
            </template>
        </Card>
        <span class="h-0" v-else />

        <ProjectsListbox />
        <NewProject />
    </div>
</template>

<style scoped lang="scss"></style>
