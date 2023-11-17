<script setup lang="ts">
import { provide } from "vue";
import PropCategory from "./PropCategory.vue";
import InlineMessage from "primevue/inlinemessage";

const props = defineProps(["controller", "logging"]);

provide("controller", props.controller);
provide("logging", props.logging);

props.logging.info(`PropertyEditor started.`, "propertyeditor");
props.logging.info(
    `${
        props.controller.getProfileIds().length
    } profiles loaded: ${JSON.stringify(props.controller.getProfileIds())}`,
    "propertyeditor"
);
</script>

<template>
    <div>
        <div v-for="profileId in props.controller.getProfileIds()">
            <div class="text-2xl bg-sky-100">
                {{ `${profileId["name"]} v${profileId["version"]}` }}
            </div>
            <div class="">
                <PropCategory
                    v-for="category in props.controller.getCategoryById(
                        profileId
                    )"
                    :category="category"
                    :profileId="profileId"
                    class="my-5"
                />
            </div>
        </div>
        <div
            v-show="!props.controller.getProfileIds().length"
            class="flex justify-center text-2xl w-full"
        >
            <InlineMessage
                v-show="!props.controller.getProfileIds().length"
                class="text-2xl"
                severity="error"
                >Could not load any metadata profiles</InlineMessage
            >
        </div>
    </div>
</template>
