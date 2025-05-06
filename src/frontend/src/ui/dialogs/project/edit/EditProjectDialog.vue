<script setup lang="ts">
import { Form } from "@primevue/forms";
import Checkbox from "primevue/checkbox";
import Fieldset from "primevue/fieldset";
import IftaLabel from "primevue/iftalabel";
import InputText from "primevue/inputtext";
import ScrollPanel from "primevue/scrollpanel";
import Step from "primevue/step";
import StepList from "primevue/steplist";
import StepPanel from "primevue/steppanel";
import StepPanels from "primevue/steppanels";
import Stepper from "primevue/stepper";
import Textarea from "primevue/textarea";
import ToggleSwitch from "primevue/toggleswitch";
import { computed, onMounted, ref, unref, watch } from "vue";
import * as yup from "yup";

import { ListResourcesReply } from "@common/api/resource/ResourceCommands";
import { resourcesListToTreeNodes } from "@common/data/entities/resource/ResourceUtils";
import { useExtendedDialogTools } from "@common/ui/dialogs/ExtendedDialogTools";
import { useDirectives } from "@common/ui/Directives";

import LegendHeader from "@common/ui/components/misc/LegendHeader.vue";
import MandatoryMark from "@common/ui/components/misc/MandatoryMark.vue";
import ResourcesTree from "@common/ui/components/resource/ResourcesTree.vue";
import StepIconHeader from "@common/ui/components/stepper/StepIconHeader.vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { type UIOptions } from "@/data/entities/ui/UIOptions";
import { ListResourcesAction } from "@/ui/actions/resource/ListResourcesAction";
import { SnapInsCatalog } from "@/ui/snapins/SnapInsCatalog";

import ConnectorInstancesSelect from "@/ui/dialogs/project/edit/ConnectorInstancesSelect.vue";
import EditProjectDialogFooter from "@/ui/dialogs/project/edit/EditProjectDialogFooter.vue";

const { dialogData, acceptDialog, useValidator } = useExtendedDialogTools();
const { vFocus } = useDirectives();

const comp = FrontendComponent.inject();
const optSnapIns = SnapInsCatalog.allOptionals();
const uiOptions = ref<UIOptions>(dialogData.userData.options.ui);
const showDataPathSelector = dialogData.options["showDataPathSelector"];
const newProject = dialogData.userData.newProject;

const stepIndices = {
    main: 0,
    datapath: 1,
    features: 2,
    connections: 3
};
const lastStepIndex = Object.entries(stepIndices).length - 1;
const activeStep = ref(stepIndices.main);

const form = ref();
const validator = useValidator(form, {
    title: yup.string().trim().required().label("Name"),
    description: yup.string().notRequired().label("Description"),
    datapath: yup
        .string()
        .test("datapath-not-empty", "No data path selected", (_, ctx) => {
            if (dialogData.userData.datapath == "") {
                return ctx.createError({ path: "datapath" });
            }
            return true;
        })
        .label("Data path")
});
const initialFormValues = ref({ title: dialogData.userData.title, description: dialogData.userData.description, datapath: dialogData.userData.datapath });

const resourcesNodes = ref<Object[]>([]);
const resourcesError = ref("");
onMounted(() => {
    if (showDataPathSelector) {
        const action = new ListResourcesAction(comp, true);
        action
            .prepare("", true, false)
            .done((reply: ListResourcesReply, success, msg) => {
                if (success) {
                    resourcesNodes.value = resourcesListToTreeNodes(reply.resources, true);
                }
            })
            .failed((_, msg) => {
                resourcesError.value = "Unable to load resources";
            });
        action.execute();
    }
});

// Reflect selected features based on snap-ins with associated project features
watch(
    () => uiOptions.value.optional_snapins,
    (snapIns) => {
        dialogData.userData.options.optional_features = SnapInsCatalog.filter(
            (snapIn) => snapIns.includes(snapIn.snapInID) && !!snapIn.options.optional?.feature
        ).map((snapIn) => snapIn.options.optional!.feature);
    }
);

const prevCallback = computed(() => {
    if (unref(activeStep) == stepIndices.main) {
        return undefined;
    } else {
        return onPrevStep;
    }
});
const nextCallback = computed(() => {
    return onNextStep;
});
const nextName = computed(() => {
    if (unref(activeStep) >= lastStepIndex) {
        return newProject ? "Create" : "Save";
    } else {
        return undefined;
    }
});

function onClickStep(event: Event, callback: (event: Event) => void) {
    validator
        .validate()
        .then(() => {
            if (callback) {
                callback(event);
            }
        })
        .catch(() => {});
}

function onPrevStep() {
    activeStep.value -= 1;
}

function onNextStep() {
    validator
        .validate()
        .then(() => {
            if (unref(activeStep) >= lastStepIndex) {
                acceptDialog();
            } else {
                activeStep.value += 1;
            }
        })
        .catch(() => {
            // Make sure to only catch errors from the current step
            if (unref(activeStep) == stepIndices.main) {
                if (validator.hasError("title")) {
                    return;
                }
            } else if (unref(activeStep) == stepIndices.datapath) {
                if (validator.hasError("datapath")) {
                    return;
                }
            }

            activeStep.value += 1;
        });
}
</script>

<template>
    <Form
        ref="form"
        :resolver="validator.resolver"
        :initial-values="initialFormValues"
        :validate-on-mount="false"
        :validate-on-blur="false"
        :validate-on-value-update="!newProject"
        @submit="!newProject ? acceptDialog : undefined"
        :class="[{ 'h-[calc(100%-4rem)]': newProject }, 'r-form']"
    >
        <Stepper v-model:value="activeStep" :linear="newProject" :dt="!newProject ? { 'separator.activeBackground': '{content.border.color}' } : {}">
            <StepList>
                <Step v-slot="{ activateCallback }" :value="stepIndices.main" :pt="{ number: 'hidden' }">
                    <StepIconHeader
                        :active="newProject ? stepIndices.main <= activeStep : stepIndices.main == activeStep"
                        :click-callback="(event: Event) => onClickStep(event, activateCallback)"
                        icon="mi-edit"
                        title="Main settings"
                    />
                </Step>

                <Step v-slot="{ activateCallback }" :value="stepIndices.datapath" :pt="{ number: 'hidden' }">
                    <StepIconHeader
                        :active="newProject ? stepIndices.datapath <= activeStep : stepIndices.datapath == activeStep"
                        :click-callback="(event: Event) => onClickStep(event, activateCallback)"
                        icon="mi-folder"
                        title="Data path"
                    />
                </Step>

                <Step v-slot="{ activateCallback }" :value="stepIndices.features" :pt="{ number: 'hidden' }">
                    <StepIconHeader
                        :active="newProject ? stepIndices.features <= activeStep : stepIndices.features == activeStep"
                        :click-callback="(event: Event) => onClickStep(event, activateCallback)"
                        icon="mi-checklist"
                        title="Additional features"
                    />
                </Step>

                <Step v-slot="{ activateCallback }" :value="stepIndices.connections" :pt="{ number: 'hidden' }">
                    <StepIconHeader
                        :active="newProject ? stepIndices.connections <= activeStep : stepIndices.connections == activeStep"
                        :click-callback="(event: Event) => onClickStep(event, activateCallback)"
                        icon="mi-hub"
                        title="Connections"
                    />
                </Step>
            </StepList>

            <StepPanels class="pt-1">
                <StepPanel :value="stepIndices.main">
                    <Fieldset legend="General settings" class="r-form-fieldset">
                        <template #legend>
                            <LegendHeader
                                title="General settings"
                                description="Set your main project settings, like its name, here. You can always change these later."
                                class="p-fieldset-legend-label"
                            />
                        </template>

                        <span class="r-form-field">
                            <IftaLabel>
                                <label>Name <MandatoryMark /></label>
                                <InputText name="title" v-model="dialogData.userData.title" fluid v-focus />
                            </IftaLabel>
                            <small>The name of the project.</small>
                        </span>

                        <span class="r-form-field mt-5">
                            <IftaLabel class="mb-[-0.5rem]">
                                <label>Description</label>
                                <Textarea name="description" v-model="dialogData.userData.description" rows="3" fluid />
                            </IftaLabel>
                            <small>The description of the project.</small>
                        </span>
                    </Fieldset>
                </StepPanel>

                <StepPanel :value="stepIndices.datapath">
                    <Fieldset legend="Data path" class="h-fit r-form-fieldset">
                        <template #legend>
                            <LegendHeader
                                title="Data path"
                                description="Select the root data path for your project here. Note that this path cannot be changed once the project has been created."
                                class="p-fieldset-legend-label"
                            >
                                <template #title>
                                    <span>Data path <MandatoryMark /></span>
                                </template>
                            </LegendHeader>
                        </template>

                        <div class="r-form-field">
                            <div v-if="showDataPathSelector" class="grid grid-flow-row">
                                <div v-if="!resourcesError" class="w-full">
                                    <small class="px-2 py-1.5 r-shade-gray rounded-lg truncated inline-block w-full">
                                        <b class="pr-1">Selected path:</b> {{ dialogData.userData.datapath || "(None)" }}
                                    </small>
                                    <ScrollPanel class="h-48">
                                        <ResourcesTree
                                            name="datapath"
                                            v-model="dialogData.userData.datapath"
                                            :options="resourcesNodes"
                                            loading
                                            expand-first-only
                                            class="w-full h-fit"
                                            @changed="validator.refresh()"
                                        />
                                    </ScrollPanel>
                                </div>
                                <div v-else class="h-fit"><b>Unable to load resources:</b> {{ resourcesError }}</div>
                            </div>
                            <div v-else class="grid grid-flow-row">
                                <span class="flex border border-solid rounded p-2">
                                    <span class="basis-0 material-icons-outlined mi-folder opacity-75 pr-2" />
                                    <span>{{ dialogData.userData.datapath }}</span>
                                </span>
                                <span>
                                    <small class="pt-3"><b>Project already created:</b> The data path cannot be changed anymore.</small>
                                </span>
                            </div>
                        </div>
                        <small class="pt-3"><b>Important:</b> This path cannot be changed after the project has been created!</small>
                    </Fieldset>
                </StepPanel>

                <StepPanel :value="stepIndices.features">
                    <Fieldset legend="Additional features" class="r-form-fieldset">
                        <template #legend>
                            <LegendHeader
                                title="Additional features"
                                description="Select additional features you want to use in this project. You can always turn these on or off later."
                                class="p-fieldset-legend-label"
                            />
                        </template>

                        <div v-for="snapIn of optSnapIns" :key="snapIn.snapInID" class="flex align-items-center pb-3">
                            <Checkbox
                                v-model="uiOptions.optional_snapins"
                                :inputId="snapIn.snapInID"
                                :value="snapIn.snapInID"
                                size="large"
                                class="self-center"
                            />
                            <label :for="snapIn.snapInID" class="pl-2 grid grid-flow-row">
                                <span class="font-bold">{{ snapIn.options.optional!.label }}</span>
                                <span v-if="!!snapIn.options.optional?.description" class="r-text-gray text-sm">{{
                                    snapIn.options.optional?.description
                                }}</span>
                            </label>
                        </div>
                    </Fieldset>
                </StepPanel>

                <StepPanel :value="stepIndices.connections">
                    <Fieldset legend="Connections" class="r-form-fieldset">
                        <template #legend>
                            <LegendHeader
                                title="Connections"
                                description="Here you can select which repository connections - all or only specific ones - to make available for uploading your project. You can always change this selection later.<p class='pt-2'>Each connection comes with its own set of required metadata fields.<p>"
                                class="p-fieldset-legend-label"
                            />
                        </template>

                        <div class="r-form-field">
                            <div class="grid grid-flow-row">
                                <div class="flex align-items-center">
                                    <ToggleSwitch
                                        v-model="dialogData.userData.options.use_all_connector_instances"
                                        inputId="useSelectConnectorInstances"
                                        :true-value="false"
                                        :false-value="true"
                                        @change="validator.refresh()"
                                        class="self-center"
                                    />
                                    <label for="useSelectConnectorInstances" class="pl-1.5">Use only the following repository connections:</label>
                                </div>

                                <div class="!h-full border border-solid rounded p-1 ml-3.5 mr-3.5 mt-1.5">
                                    <ConnectorInstancesSelect
                                        v-model="dialogData.userData.options.active_connector_instances"
                                        :disabled="dialogData.userData.options.use_all_connector_instances"
                                        class="w-full h-60"
                                    />
                                </div>
                            </div>
                        </div>
                    </Fieldset>
                </StepPanel>
            </StepPanels>
        </Stepper>
    </Form>

    <EditProjectDialogFooter
        v-if="newProject"
        :prev-callback="prevCallback"
        :next-callback="nextCallback"
        :next-name="nextName"
        :next-icon="activeStep >= lastStepIndex ? 'mi-done' : undefined"
        :next-icon-position="activeStep >= lastStepIndex ? 'left' : undefined"
        class="mt-auto"
    />
</template>

<style scoped lang="scss"></style>
