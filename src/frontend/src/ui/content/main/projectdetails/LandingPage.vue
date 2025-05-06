<script setup lang="ts">
import Card from "primevue/card";

import ExternalLink from "@common/ui/components/misc/ExternalLink.vue";

import { FrontendComponent } from "@/component/FrontendComponent.ts";

const comp = FrontendComponent.inject();
</script>

<template>
    <div>
        <div class="r-shade-text m-10 !mb-0 !pb-0">
            <div class="grid grid-cols-2 min-w-full min-h-full place-content-start gap-24 pb-0">
                <div class="space-y-4 !pb-0">
                    <div>
                        <div class="text font-light uppercase">{{ comp.data.title }}</div>
                        <div class="text-4xl font-black uppercase leading-none">
                            Research data <span class="font-thin text-nowrap text-3xl">made easy</span>
                        </div>
                    </div>
                    <div class="text-lg font-light mb-1">
                        Your flexible solution for research data managing and uploading. The services are designed to make data management effortless and
                        collaborative, so you can focus on what matters most: <span class="italic">your research</span>.
                        <div class="pt-2 text-lg">
                            Learn more:
                            <ExternalLink link="https://github.com/Sciebo-RDS" text="GitHub repository" />
                        </div>
                    </div>
                    <Card class="p-2 h-fit" :pt="{ body: '!pb-0' }">
                        <template #content>
                            <div class="grid justify-items-center">
                                <img src="@assets/img/rds-steps-web.png" class="h-full max-h-[calc(100vh-30rem)]" alt="Steps" />
                            </div>
                        </template>
                    </Card>
                </div>

                <div class="grid place-items-center max-w-fit space-y-4">
                    <img src="@assets/img/landing_image.png" class="w-[25rem]" alt="Image" />
                    <Card class="w-[30rem] bg-amber-50 text-amber-600">
                        <template #title>
                            <div class="flex items-center gap-1">
                                <span class="material-icons-outlined mi-construction" />
                                <span class="">This is a beta version!</span>
                            </div>
                        </template>
                        <template #content>
                            This version of {{ comp.data.title }} is still under construction. If you encounter any issues or have other kinds of feedback, feel
                            free to
                            <ExternalLink link="mailto:sciebo.rds@uni-muenster.de" text="send us an email" internal />
                            !
                        </template>
                    </Card>
                    <Card class="w-[30rem]">
                        <template #title>
                            <div class="">Here's how we support you:</div>
                        </template>
                        <template #content>
                            <ul class="pl-6 list-outside list-disc">
                                <li class="">
                                    <strong>Configure research processes -</strong> A research data tool in your cloud that flexibly adapts to your individual
                                    research workflows.
                                </li>
                                <li class="">
                                    <strong>Project Workflow Integration -</strong> A research data tool that connects existing research data services according
                                    to your needs.
                                </li>
                                <li class="">
                                    <strong>User Control -</strong> Full control over your data, with clear options to manage access, set metadata and
                                    conditions for sharing.
                                </li>
                                <li class="">
                                    <strong>Ease of Use -</strong> Intuitive services that integrate smoothly into your daily research activities, saving you
                                    time and effort.
                                </li>
                            </ul>
                        </template>
                    </Card>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">
div {
    @apply pb-4;
}
</style>
