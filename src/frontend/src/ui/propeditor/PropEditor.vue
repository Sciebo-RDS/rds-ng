<script setup lang="ts">
import { provide, type PropType } from "vue";
import PropCategory from "./PropCategory.vue";
import InlineMessage from "primevue/inlinemessage";
import { Logger } from "./utils/Logging";
import { PropertyController } from "@/ui/propeditor/PropertyController";

const props = defineProps({
    controller: {
        type: Object as PropType<PropertyController>,
        required: true,
    },
    logging: {
        type: Object as PropType<Logger>,
        default: null,
    },
});
const logging = props.logging || Logger;

provide("controller", props.controller);
provide("logging", logging);

logging.info(`PropertyEditor started.`, "propertyeditor");

if (props.controller.getProfileIds().length) {
    logging.info(
        `Loaded ${
            props.controller.getProfileIds().length
        } profiles: ${JSON.stringify(props.controller.getProfileIds())}`,
        "propertyeditor"
    );
} else {
    logging.warning(`Could not load any metadata Profiles.`, "propertyeditor");
}
</script>

<template>
    <div class="overflow-hidden">
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
