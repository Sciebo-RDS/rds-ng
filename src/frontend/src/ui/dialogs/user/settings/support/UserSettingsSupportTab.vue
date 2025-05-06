<script setup lang="ts">
import { FrontendComponent } from "@/component/FrontendComponent";
import Message from "primevue/message";
import { type PropType, toRefs } from "vue";

import { UserSettings } from "@common/data/entities/user/UserSettings";

import ExternalLink from "@common/ui/components/misc/ExternalLink.vue";

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
                <img id="logo" src="@assets/img/rds-octopus-bl.svg" alt="RDS Logo" class="p-1.5" width="75rem" title="Visit the RDS website" />
            </a>
            <div>
                {{ comp.data.title }} allows researchers to export research data directly from their cloud storage systems to data repositories and external
                storages.
            </div>
        </div>
        <Message severity="warn" icon="material-icons-outlined mi-warning-amber mr-1 mb-0.5" :closable="false" class="text-sm my-4">
            This is an <em>early preview version</em> of the final application. If you encounter any issues or have some feedback, feel free to
            <ExternalLink link="mailto:sciebo.rds@uni-muenster.de" text="send us an email" internal />
            !
        </Message>

        <div class="r-text-caption mt-1">Links</div>
        <div class="grid grid-flow-rows">
            <ExternalLink link="https://www.research-data-services.org" text="Official website" />
            <ExternalLink link="https://github.com/Sciebo-RDS" text="GitHub repository" />
        </div>

        <div class="r-text-caption mt-1">Bug reporting &amp; Suggestions</div>
        If you're running into any issues or have further suggestions, use the following link to create an issue on our GitHub repository:
        <ExternalLink link="https://github.com/Sciebo-RDS/rds-ng/issues" />

        <div class="r-text-caption mt-3">Version</div>
        <div>{{ comp.data.title }} - Version {{ comp.data.version }}</div>

        <div class="r-text-caption mt-3">About</div>
        <div class="grid grid-cols-[max-content_max-content_max-content] items-center">
            {{ comp.data.title }} Copyright &copy;&nbsp;
            <ExternalLink link="https://www.uni-muenster.de" text="University of Muenster" />
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
