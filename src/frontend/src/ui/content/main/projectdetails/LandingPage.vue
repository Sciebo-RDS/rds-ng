<script setup lang="ts">
import Card from "primevue/card";
import ScrollPanel from "primevue/scrollpanel";

import LinkedText from "@common/ui/components/misc/LinkedText.vue";

import { FrontendComponent } from "@/component/FrontendComponent.ts";

const comp = FrontendComponent.inject();
</script>

<template>
    <ScrollPanel class="w-full h-[calc(100vh)]">
        <div class="grid grid-rows-[min-content_auto_auto] r-shade-text mx-14 max-w-[80rem]">
            <Card class="bg-amber-100 text-amber-700 !p-0 mt-4 w-full h-min" :pt="{ title: '!text-base', caption: 'h-5', body: 'p-2 px-4' }">
                <template #title>
                    <div class="flex items-center gap-1">
                        <span class="material-icons-outlined mi-construction !text-xl" />
                        <span class="">This is a beta version!</span>
                        <span class="text-sm font-normal pl-0.5">
                            If you encounter any issues or have other kinds of feedback, feel free to
                            <LinkedText link="mailto:sciebo.rds@uni-muenster.de" text="send us an email" />
                            !
                        </span>
                    </div>
                </template>
                <template #content></template>
            </Card>
            <div class="flex flex-row !pb-0">
                <div class="flex flex-col">
                    <div class="text-3xl font-bold mt-8">Hello, I'm {{ comp.data.title }}!</div>
                    <div class="text-lg font-bold">Your assistant for easy and secure research data sharing.</div>
                    <div>&nbsp;</div>
                    <div>I'm here to help you manage, prepare, and share your research data - flexibly, securely, and in line with your workflows.</div>
                    <div>My goal: making your data handling easier and safe, so you can stay focused on your research.</div>
                </div>
                <div class="ml-auto !pb-0">
                    <img src="@assets/img/octopus.svg" alt="logo" class="w-[28rem]" />
                </div>
            </div>

            <div class="mr-6 mb-12 justify-self-center">
                <Card class="bg-primary-50 justify-self-center" :pt="{ body: 'pt-4 pb-0 px-0', content: 'grid justify-self-center mx-[-2rem]' }">
                    <template #content>
                        <img src="@assets/img/landing-steps.svg" class="w-[92%] justify-self-center self-center" alt="First steps" />
                    </template>
                </Card>
            </div>
        </div>
    </ScrollPanel>
</template>

<style scoped lang="scss">
div {
    @apply pb-4;
}
</style>
