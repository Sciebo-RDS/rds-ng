<script setup lang="ts">
import { type PropType, toRefs } from "vue";

const props = defineProps({
    errors: {
        type: Object as PropType<String[]>,
        required: true
    }
});
const { errors } = toRefs(props);
</script>

<template>
    <span class="font-bold">One or more fields are missing or invalid:</span>
    <br />
    <span class="italic">
        {{ errors[0] }}
        <span v-if="errors.length > 1" :title="errors.join('\n')">
            (+ <b>{{ errors.length - 1 }} more</b>)
        </span>
    </span>
</template>

<style scoped lang="scss"></style>
