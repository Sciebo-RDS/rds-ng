<script setup lang="ts">
import { Form } from "@primevue/forms";
import Fieldset from "primevue/fieldset";
import IftaLabel from "primevue/iftalabel";
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
    token: dialogData.userData.bearerToken
});

function getValidatorShape(): any {
    const token = yup.string().trim().required().label(dialogData.userData.config.bearer_label);

    return { token: token };
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
        <div>The external services requires you to provide an access token in order to be used.</div>
        <div v-if="!!dialogData.userData.config.help_link">
            For further information about how to get this token, you can visit
            <LinkedText :link="dialogData.userData.config.help_link" text="this link" /> which will provide additional help.
        </div>

        <Fieldset legend="Token" class="r-form-fieldset">
            <span class="r-form-field">
                <IftaLabel>
                    <Password name="token" v-model.trim="dialogData.userData.bearerToken" :feedback="false" toggle-mask fluid autofocus />
                    <label>{{ dialogData.userData.config.bearer_label }} <MandatoryMark /></label>
                </IftaLabel>
                <small>The {{ dialogData.userData.config.bearer_label.toLowerCase() }} for the external service.</small>
            </span>
        </Fieldset>
    </Form>
</template>

<style scoped lang="scss"></style>
