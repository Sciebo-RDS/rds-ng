<script setup>
import { toRefs } from "vue";

const props = defineProps({
    link: {
        type: String,
        required: true,
    },
    text: {
        type: String,
    },
});
const { link, text } = toRefs(props);
</script>

<template>
    <span class="r-text-link inline-block">
        <a :href="link" class="grid grid-cols-[max-content_min-content] items-center" target="_blank">
            {{ text || link }}
            <span class="material-icons-outlined mi-open-in-new ml-1 !text-lg" />
        </a>
    </span>
</template>

<style scoped lang="scss"></style>
