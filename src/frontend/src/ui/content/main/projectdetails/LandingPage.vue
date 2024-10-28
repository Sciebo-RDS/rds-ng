<script setup lang="ts">
import Card from "primevue/card";

import ExternalLink from "@common/ui/components/misc/ExternalLink.vue";
</script>

<template>
    <div class="bg-slate-50">
        <div class="content-center r-shade-text m-10">
            <div class="grid grid-cols-2 min-w-full min-h-full place-content-center">
                <div class="space-y-8">
                    <div>
                        <div class="text font-light uppercase">Sciebo Research Data Services</div>
                        <div class="text-[3rem] font-black uppercase leading-none">Research data made easy</div>
                    </div>
                    <div class="text-[1.2rem] font-light mb-10">
                        Your flexible solution for research data managing and publishing. The services are designed to make data management effortless and
                        collaborative, so you can focus on what matters most: your research.
                        <div class="pl-2">
                            Learn more:
                            <ExternalLink link="https://github.com/Sciebo-RDS" text="GitHub repository" />
                        </div>
                    </div>
                    <Card>
                        <template #content>
                            <img src="@assets/img/rds-steps-web.png" class="justify-self-center" />
                        </template>
                    </Card>
                </div>
                <!-- ... -->
                <div class="grid place-items-center space-y-7">
                    <img src="@assets/img/image.png" class="w-[25rem]" />
                    <Card class="w-[30rem]">
                        <template #title><div class="">Here's how we support you</div></template>
                        <template #content>
                            <ul class="pl-6 list-outside list-disc">
                                <li class="">
                                    <strong>Configure research processes -</strong> A research data tool in your cloud that flexibly adapts to your individual
                                    research workflows.
                                </li>
                                <li class="">
                                    <strong>Project Workflow Integration -</strong> A research data tool that connects existing research data services according
                                    to your needs
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
