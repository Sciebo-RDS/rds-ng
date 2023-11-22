<script setup lang="ts">
import InputText from "primevue/inputtext";
import Textarea from "primevue/textarea";

import { useDirectives } from "@common/ui/Directives";
import { extendedDialogTools } from "@common/ui/dialogs/ExtendedDialogTools";

import { FrontendComponent } from "@/component/FrontendComponent";

const { dialogData, acceptDialog } = extendedDialogTools();
const { vFocus } = useDirectives();

const comp = FrontendComponent.inject();
</script>

<template>
    <form @submit.prevent="acceptDialog" class="r-form pt-5">
        <span class="r-form-field">
            <label>Title</label>
            <InputText v-model="dialogData.userData.title" placeholder="Title" v-focus />
            <small>The title of the project.</small>
        </span>

        <span class="r-form-field">
            <label>Description</label>
            <Textarea v-model="dialogData.userData.description" placeholder="Description" rows="3" />
            <small>An (optional) project description.</small>
        </span>
    </form>
</template>

<style scoped lang="scss">
</style>
