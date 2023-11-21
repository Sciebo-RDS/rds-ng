<script setup lang="ts">
import InputText from "primevue/inputtext";
import Textarea from "primevue/textarea";
import { ref } from "vue";

import { editDialogHandling } from "@common/ui/dialogs/EditDialogHandling";

import { FrontendComponent } from "@/component/FrontendComponent";

const { dialogData, acceptDialog, autoFocus } = editDialogHandling();

const comp = FrontendComponent.inject();

// Focus the first element on load
const titleElement = ref();
autoFocus(titleElement);
</script>

<template>
    <!-- TODO: Make pretty <3 -->
    <form @submit.prevent="acceptDialog">
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
