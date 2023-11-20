<script setup lang="ts">
import { FrontendComponent } from "@/component/FrontendComponent";
import InputText from "primevue/inputtext";
import { ref, watch } from "vue";

const comp = FrontendComponent.inject();

const text = ref("THIS IS WSPA");
watch(text, (o, n) => {
    console.log(o + "---" + n);
});
</script>

<template>
    <ConfirmDialog group="templating">
        <template #message="slotProps">
            <div class="flex flex-column align-items-center w-full gap-3 border-bottom-1 surface-border">
                <i :class="slotProps.message.icon" class="text-6xl text-primary-500"></i>
                <p>{{ slotProps.message.message }}</p>
                <div>
                    <InputText v-model="text"></InputText>
                </div>
            </div>
        </template>
    </ConfirmDialog>
</template>

<style scoped lang="scss">

</style>
