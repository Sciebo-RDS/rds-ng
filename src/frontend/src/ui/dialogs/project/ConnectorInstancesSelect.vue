<script setup lang="ts">
import Checkbox from "primevue/checkbox";
import ScrollPanel from "primevue/scrollpanel";
import { toRefs } from "vue";

import { useUserStore } from "@/data/stores/UserStore";

const userStore = useUserStore();
const { userSettings } = toRefs(userStore);
const props = defineProps({
    disabled: {
        type: Boolean,
        default: false
    }
});
const { disabled } = toRefs(props);
const model = defineModel({ default: [] });
</script>

<template>
    <ScrollPanel class="w-full h-[7.5rem]">
        <div v-for="instance of userSettings.connector_instances" :key="instance.instance_id" class="flex align-items-center">
            <Checkbox
                v-model="model"
                :inputId="instance.instance_id"
                :value="instance.instance_id"
                :disabled="disabled"
            />
            <label :for="instance.instance_id" :class="{ 'p-disabled': disabled }">{{ instance.name }}</label>
        </div>
    </ScrollPanel>
</template>

<style scoped lang="scss">

</style>
