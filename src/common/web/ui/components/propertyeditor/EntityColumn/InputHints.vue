<script setup lang="ts">
import LinkedText from "@common/ui/components/misc/LinkedText.vue";

const { hintLink, hintText } = defineProps(["hintLink", "hintText"]);
</script>

<template>
    <div>
        <span class="text-gray-500 mr-2" v-if="!!hintText">{{ hintText }}</span>
        <LinkedText v-if="!!hintLink.url && !!hintLink.label" :link="hintLink.url" :text="hintLink.label" />
    </div>
</template>
