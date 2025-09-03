<script setup lang="ts">
import Card from "primevue/card";
import { type PropType, toRefs } from "vue";

import { UserSettings } from "@common/data/entities/user/UserSettings";
import { GeneralSettingIDs } from "@common/settings/GeneralSettingIDs.ts";

import LinkedText from "@common/ui/components/misc/LinkedText.vue";

import { FrontendComponent } from "@/component/FrontendComponent";

const comp = FrontendComponent.inject();
const props = defineProps({
    tabData: {
        type: Object as PropType<UserSettings>,
        required: true
    }
});
const propRefs = toRefs(props);
</script>

<template>
    <div class="grid grid-rows-[auto_auto_1fr_auto] grid-cols-1 gap-1.5 w-full h-full">
        <div class="r-text-title">About</div>
        <div class="r-text-caption">Welcome to {{ comp.data.title }}!</div>
        <div class="grid grid-cols-[max-content_1fr] gap-1.5 items-center w-full">
            <a href="https://www.research-data-services.org" target="_blank">
                <img id="logo" src="@assets/img/logo-bridgit.png" alt="bridgit logo" class="p-1.5 w-52 brightness-0" title="Visit the RDS website" />
            </a>
            <div>
                {{ comp.data.title }} allows researchers to export research data directly from their cloud storage systems to data repositories and external
                storages.
            </div>
        </div>
        <Card class="bg-amber-100 text-amber-700 !p-0 mt-4 mb-4 w-fit" :pt="{ title: '!text-base', caption: 'h-5', body: 'p-3 px-5' }">
            <template #title>
                <div class="flex items-center gap-1">
                    <span class="material-icons-outlined mi-construction !text-xl" />
                    <span class="">This is a beta version!</span>
                </div>
            </template>
            <template #content>
                <span class="text-sm">
                    If you encounter any issues or have other kinds of feedback, feel free to
                    <LinkedText :link="`mailto:${comp.data.config.value<string>(GeneralSettingIDs.SupportEmail)}`" text="send us an email" />
                    !
                </span>
            </template>
        </Card>

        <div class="r-text-caption mt-1">Links</div>
        <div class="grid grid-flow-rows">
            <LinkedText link="https://www.research-data-services.org" text="Official website" />
            <LinkedText link="https://github.com/Sciebo-RDS" text="GitHub repository" />
        </div>

        <div class="r-text-caption mt-1">Bug reporting &amp; Suggestions</div>
        If you're running into any issues or have further suggestions, use the following link to create an issue on our GitHub repository:
        <LinkedText link="https://github.com/Sciebo-RDS/rds-ng/issues" />

        <div class="r-text-caption mt-3">Version</div>
        <div>{{ comp.data.title }} - Version {{ comp.data.version }}</div>

        <div class="r-text-caption mt-3">About</div>
        <div class="grid grid-cols-[max-content_max-content_max-content] items-center">
            {{ comp.data.title }} Copyright &copy;&nbsp;
            <LinkedText link="https://www.uni-muenster.de" text="University of Muenster" />
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
