<script setup lang="ts">
import { computed, type Ref, ref } from "vue";

import Button from "primevue/button";
import Chip from "primevue/chip";
import Dialog from "primevue/dialog";
import FloatLabel from "primevue/floatlabel";
import InputText from "primevue/inputtext";
import OrderList from "primevue/orderlist";

import { useColorsStore } from "../../../data/stores/ColorsStore";
import { ProfileLayoutClass } from "./PropertyProfile";

const visible = defineModel("visible") as Ref<boolean>;
const props = defineProps(["hiddenProperties"]);
const emit = defineEmits(["addProperties"]);
const colorsStore = useColorsStore();

const searchString = ref("");
const selectedProperties = ref([]) as Ref<ProfileLayoutClass[]>;
const resetDialog = () => {
    selectedProperties.value = [];
    searchString.value = "";
};
const updateSelectedProperties = (selection: ProfileLayoutClass[]) => (selectedProperties.value = selection);

const filteredProperties = computed(() =>
    props.hiddenProperties.filter(
        (e: ProfileLayoutClass) =>
            e.getDisplayLabel().toLowerCase().includes(searchString.value.toLowerCase()) ||
            e.getDescription()?.toLowerCase().includes(searchString.value.toLowerCase())
    )
);
</script>

<template>
    <Dialog
        v-model:visible="visible"
        modal
        header="Add properties"
        :pt="{ content: 'h-full' }"
        :style="{ width: '50vw', height: '80vh' }"
        @after-hide="resetDialog()"
    >
        <template #default>
            <div class="h-full flex-col flex space-y-4">
                <FloatLabel>
                    <InputText type="text" v-model="searchString" id="searchString" class="w-full" />
                    <label for="searchString">Search...</label>
                </FloatLabel>
                <OrderList
                    v-model="filteredProperties"
                    @update:selection="(selection: ProfileLayoutClass[]) => updateSelectedProperties(selection)"
                    dataKey="id"
                    class="h-full select-none"
                    :pt="{ pcListbox: { root: 'w-full', listContainer: 'min-h-full' } }"
                    :stripedRows="true"
                >
                    <template #option="slotProps">
                        <div class="flex flex-col w-full p-1" :title="slotProps.option.getDescription()">
                            <span class="font-semibold flex gap-2">
                                <span class="grow"> {{ slotProps.option.getDisplayLabel() }}</span>
                                <Chip
                                    v-for="p in slotProps.option.getProfiles()"
                                    :label="p[0]"
                                    size="small"
                                    :style="`background-color: ${colorsStore.color(p[0])}`"
                                    class="h-4 !rounded py-3 text-sm bg-opacity-40"
                            /></span>
                            <span class="text-gray-500 ellipsis line-clamp-1">{{ slotProps.option.getDescription() }}</span>
                        </div>
                    </template>
                </OrderList>
            </div>
        </template>
        <template #footer>
            <div class="flex justify-end gap-2 mt-5">
                <Button
                    :disabled="!selectedProperties.length"
                    @click="
                        emit('addProperties', selectedProperties);
                        resetDialog();
                        visible = false;
                    "
                    >Add {{ selectedProperties.length ? "(" + selectedProperties.length + ")" : "" }}
                </Button>
                <Button
                    outlined
                    severity="secondary"
                    @click="
                        resetDialog();
                        visible = false;
                    "
                    >Cancel
                </Button>
            </div>
        </template>
    </Dialog>
</template>

<style scoped lang="scss">
:deep(.p-orderlist-controls) {
    display: none;
}

:deep(.p-orderlist-item) {
    @apply border-l-2 border-solid border-transparent;
}

:deep(.p-orderlist-item.p-highlight) {
    @apply bg-emerald-50  border-l-2 border-emerald-600 text-slate-700;
}
</style>
