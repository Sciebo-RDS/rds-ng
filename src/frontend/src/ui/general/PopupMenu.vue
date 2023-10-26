<script setup lang="ts">
import { ref, toRefs, watch } from "vue";

import Menu from "primevue/menu";

// TODO: Better way to expose "isShown"? Emit?
// TODO: Move to common

const props = defineProps(['items', 'activator', 'isShown']);
const state = toRefs(props);
const items = state.items;
const activator = state.activator;

const popupMenu = ref();
const popupMenuShown = ref(false);

watch(activator, (event) => {
    popupMenu?.value.toggle(event);
});
watch(popupMenuShown, (shown) => {
    if (state.isShown) {
        state.isShown.value = shown;
    }
})
</script>

<template>
    <Menu ref="popupMenu" :model="items" :popup="true" @focus="popupMenuShown=true" @blur="popupMenuShown=false">
        <template #item="{ item, label, props }">
            <a class="flex" v-bind="props.action">
                <span v-bind="props.icon" :class="['material-icons-outlined', item.color ? `!${item.color}` : '']">{{ item.icon }}</span>
                <span v-bind="props.label" :class="['pt-0.5', item.color ? `!${item.color}` : '']">{{ label }}</span>
            </a>
        </template>
    </Menu>
</template>

<style scoped lang="scss">
</style>
