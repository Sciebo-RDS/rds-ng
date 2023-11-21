<script setup lang="ts">
import { editDialogHandling } from "@common/ui/dialogs/EditDialogHandling";
import InputText from "primevue/inputtext";
import Textarea from "primevue/textarea";
import { ref, watch } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";

const { dialogData, acceptDialog } = editDialogHandling();

const comp = FrontendComponent.inject();

// Focus the first element on load
const titleElement = ref();
watch(titleElement, () => {
    titleElement.value.$el.focus();
});
</script>

<template>
    <!-- TODO: Make pretty <3 -->
    <form @submit="(event) => { event.preventDefault(); acceptDialog(); }">
        <div class="grid grid-rows-auto grid-cols-[min-content_1fr] gap-5 pt-5">
            <label>Title</label>
            <InputText ref="titleElement" v-model="dialogData.userData.title" placeholder="Title" />

            <label>Description</label>
            <Textarea v-model="dialogData.userData.description" placeholder="Description" rows="3" />
        </div>
    </form>
</template>

<style scoped lang="scss">

</style>
