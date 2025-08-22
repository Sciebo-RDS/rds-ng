<script setup>
import { toRefs } from "vue";

const props = defineProps({
    text: {
        type: String,
        default: ""
    },
    link: {
        type: String,
        default: ""
    },
    internal: {
        type: Boolean,
        default: false
    },
    iconClass: {
        type: String,
        default: "material-icons-outlined mi-open-in-new"
    }
});
const { text, link, internal, iconClass } = toRefs(props);
</script>

<template>
    <span class="r-text-link inline-block">
        <a v-if="!!link" :href="link" class="link-text" :target="!internal ? '_blank' : ''">
            {{ text || link }}
            <span class="link-icon" :class="iconClass" />
        </a>
        <span v-else class="link-text cursor-pointer">
            {{ text }}
            <span class="link-icon" :class="iconClass" />
        </span>
    </span>
</template>

<style scoped lang="scss">
.link-text {
    @apply grid grid-cols-[max-content_min-content] items-center cursor-pointer;
}

.link-icon {
    @apply ml-1 text-lg #{!important};
}
</style>
