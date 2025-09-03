<script setup lang="ts">
import { Form } from "@primevue/forms";
import Fieldset from "primevue/fieldset";
import IftaLabel from "primevue/iftalabel";
import InputText from "primevue/inputtext";
import Textarea from "primevue/textarea";
import { ref } from "vue";
import * as yup from "yup";

import { useExtendedDialogTools } from "@common/ui/dialogs/ExtendedDialogTools";

import MandatoryMark from "@common/ui/components/misc/MandatoryMark.vue";

const { dialogData, acceptDialog, useValidator } = useExtendedDialogTools();

const form = ref();
const validator = useValidator(form, {
    name: yup.string().trim().required().label("Name"),
    description: yup.string().notRequired().label("Description")
});
const initialFormValues = ref({
    name: dialogData.userData.name,
    description: dialogData.userData.description
});
</script>

<template>
    <Form
        ref="form"
        :resolver="validator.resolver"
        :initial-values="initialFormValues"
        :validate-on-mount="false"
        :validate-on-blur="false"
        :validate-on-value-update="true"
        @submit="acceptDialog"
        class="r-form"
    >
        <Fieldset legend="General" class="r-form-fieldset">
            <span class="r-form-field">
                <IftaLabel>
                    <InputText name="name" v-model="dialogData.userData.name" fluid autofocus />
                    <label>Name <MandatoryMark /></label>
                </IftaLabel>
                <small>The name of the connection.</small>
            </span>

            <span class="r-form-field mt-5">
                <IftaLabel class="mb-[-0.5rem]">
                    <Textarea name="description" v-model.trim="dialogData.userData.description" rows="3" fluid />
                    <label>Description</label>
                </IftaLabel>
                <small>The description of the connection.</small>
            </span>
        </Fieldset>
    </Form>

    <div v-if="dialogData.userData.requiresAuth" class="mt-5 text-sm">
        <b>Note:</b> The connection to this external service must first be authorized. A popup will open automatically after creating the new connection where
        you can log in to the external service and grant access to it.
    </div>
</template>

<style scoped lang="scss"></style>
