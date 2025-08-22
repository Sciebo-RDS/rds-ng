<script setup lang="ts">
import MultiSelect from "primevue/multiselect";
import { type PropType, toRefs } from "vue";

import { MetadataProfileContainer, type MetadataProfileContainerList } from "@common/data/entities/metadata/MetadataProfileContainer.ts";
import { useColorsStore } from "@common/data/stores/ColorsStore.ts";
import { type ProfileID } from "@common/ui/components/propertyeditor/PropertyProfile.ts";

const props = defineProps({
    profiles: {
        type: Object as PropType<MetadataProfileContainerList>,
        required: true
    }
});
const { profiles } = toRefs(props);
const selectedProfiles = defineModel<ProfileID[]>("selectedProfiles", { default: [] });

const colorsStore = useColorsStore();
</script>

<template>
    <div class="grid grid-cols-[max-content_1fr] gap-1">
        <span class="flex items-center gap-0.5 text-sm">
            <span class="material-icons-outlined mi-ballot" />
            <span class="font-bold pr-1">Metadata profiles</span>
        </span>
        <MultiSelect
            v-model="selectedProfiles"
            :options="profiles.sort((profile1, profile2) => profile1.profile.getDisplayLabel().localeCompare(profile2.profile.getDisplayLabel()))"
            :optionLabel="(option: MetadataProfileContainer) => option.profile.getDisplayLabel()"
            :optionValue="(option: MetadataProfileContainer) => option.profile.getId()"
            display="chip"
            filter
            placeholder="No additional metadata profiles selected"
            class="w-full"
        >
            <template #option="slotProps">
                <div class="grid grid-cols-[max-content_1fr] gap-1 w-full">
                    <div>{{ slotProps.option.profile.getDisplayLabel() }}</div>
                    <div class="r-text-light-gray">{{ slotProps.option.profile.getDescription() }}</div>
                </div>
            </template>
        </MultiSelect>
    </div>
</template>

<style scoped lang="scss"></style>
