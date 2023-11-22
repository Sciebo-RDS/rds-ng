<script setup lang="ts">
import InputText from "primevue/inputtext";
import Textarea from "primevue/textarea";
import { string as ystring } from "yup";

import { useDirectives } from "@common/ui/Directives";
import { extendedDialogTools } from "@common/ui/dialogs/ExtendedDialogTools";
import FieldLabel from "@common/ui/forms/FieldLabel.vue";

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
            <FieldLabel title="Title" mandatory />
            <InputText name="title" v-bind="title" v-model="dialogData.userData.title" placeholder="Title" :class="{ 'p-invalid': validator.errors.title }" v-focus />
            <small>The title of the project.</small>
        </span>

        <span class="r-form-field">
            <FieldLabel title="Description" />
            <Textarea name="description" v-model="dialogData.userData.description" placeholder="Description" rows="3" />
            <small>An (optional) project description.</small>
        </span>
    </form>
</template>

<style scoped lang="scss">
</style>
