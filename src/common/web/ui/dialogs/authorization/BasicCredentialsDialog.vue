<script setup lang="ts">
import { Form } from "@primevue/forms";
import Fieldset from "primevue/fieldset";
import IftaLabel from "primevue/iftalabel";
import InputText from "primevue/inputtext";
import Password from "primevue/password";
import { ref } from "vue";
import * as yup from "yup";

import { useExtendedDialogTools } from "../ExtendedDialogTools";

import LinkedText from "../../components/misc/LinkedText.vue";
import MandatoryMark from "../../components/misc/MandatoryMark.vue";

const { dialogData, acceptDialog, useValidator } = useExtendedDialogTools();

const form = ref();
const validator = useValidator(form, getValidatorShape());
const initialFormValues = ref({
    name: dialogData.userData.userName,
    password: dialogData.userData.userPassword
});

function getValidatorShape(): any {
    const name = yup.string().trim().required().label(dialogData.userData.config.user_id_label);
    const password = yup.string().required().label(dialogData.userData.config.user_password_label);

    return { name: name, password: password };
}
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
        <div>The external services requires you to provide account credentials in order to be used.</div>
        <div v-if="!!dialogData.userData.config.help_link">
            For further information about how to get these credentials, you can visit
            <LinkedText :link="dialogData.userData.config.help_link" text="this link" /> which will provide additional help.
        </div>

        <Fieldset legend="Credentials" class="r-form-fieldset">
            <span class="r-form-field">
                <IftaLabel>
                    <InputText name="name" v-model.trim="dialogData.userData.userName" fluid autofocus />
                    <label>{{ dialogData.userData.config.user_id_label }} <MandatoryMark /></label>
                </IftaLabel>
                <small>The {{ dialogData.userData.config.user_id_label.toLowerCase() }} for the external service.</small>
            </span>

            <span class="r-form-field mt-5">
                <IftaLabel>
                    <Password name="password" v-model.trim="dialogData.userData.userPassword" :feedback="false" toggle-mask fluid autofocus />
                    <label>{{ dialogData.userData.config.user_password_label }} <MandatoryMark /></label>
                </IftaLabel>
                <small>The {{ dialogData.userData.config.user_password_label.toLowerCase() }} for the external service.</small>
            </span>
        </Fieldset>
    </Form>
</template>

<style scoped lang="scss"></style>
