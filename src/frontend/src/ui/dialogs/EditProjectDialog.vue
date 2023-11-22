<script setup lang="ts">
import InlineMessage from "primevue/inlinemessage";
import InputText from "primevue/inputtext";
import Textarea from "primevue/textarea";
import { string as ystring } from "yup";

import { useDirectives } from "@common/ui/Directives";
import { extendedDialogTools } from "@common/ui/dialogs/ExtendedDialogTools";

import { FrontendComponent } from "@/component/FrontendComponent";

const { dialogData, acceptDialog, useValidator } = extendedDialogTools();
const { vFocus } = useDirectives();

const comp = FrontendComponent.inject();

const validator = useValidator({
    title: ystring().required().label("Title")
});
const title = validator.defineComponentBinds("title");
</script>

<template>
    <form @submit.prevent="acceptDialog" class="r-form pt-5">
        <span class="r-form-field">
            <label>Title</label>
            <InputText v-bind="title" v-model="dialogData.userData.title" placeholder="Title" :class="{ 'p-invalid': validator.errors.title }" v-focus />
            <InlineMessage v-if="validator.errors.title">{{ validator.errors.title }}</InlineMessage>
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
