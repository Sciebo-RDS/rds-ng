<script setup lang="ts">
import { type Ref } from "vue";

import Chip from "primevue/chip";
import IconField from "primevue/iconfield";
import InputIcon from "primevue/inputicon";
import InputSwitch from "primevue/inputswitch";
import InputText from "primevue/inputtext";
import { type ProfileID } from "./PropertyProfile";

const props = defineProps(["projectProfiles", "propertyObjects"]);

const searchString = defineModel("searchString") as Ref<string>;
const profileFilter = defineModel("profileFilter") as Ref<ProfileID[]>;
const requiredOnly = defineModel("requiredOnly") as Ref<boolean>;
const matchesCount = defineModel("matchesCount") as Ref<number>;
const allCount = defineModel("allCount") as Ref<number>;

const resetSearch = () => {
    searchString.value = "";
};

const resetFilters = () => {
    profileFilter.value = [];
    resetSearch();
    requiredOnly.value = false;
};
</script>

<template>
    <div class="m-5 mb-5 mr-2" :class="props.projectProfiles.list().length > 1 ? 'border-b' : ''">
        <!-- Searchbar -->
        <IconField iconPosition="left">
            <InputIcon class="pi pi-search"> </InputIcon>
            <InputText
                type="text"
                v-model="searchString"
                id="searchString"
                class="w-full"
                placeholder="Search metadata fields..."
                autocomplete="off"
                @keydown.esc="resetSearch()"
            />
            <InputIcon
                @click.stop="resetSearch()"
                disabled="!searchstring"
                class="pi pi-times-circle"
                :class="{ 'hover:text-red-400': !!searchString }"
                title="Reset search"
            />
        </IconField>

        <!-- Filters -->
        <div class="my-3 flex justify-between w-full">
            <span v-if="props.projectProfiles.list().length > 1" class="flex align-center gap-2">
                <Chip
                    :label="`All (${allCount})`"
                    title="Show all properties"
                    class="h-4 !rounded py-3 text-sm border border-slate-700 cursor-pointer select-none"
                    :class="profileFilter.length === 0 && !searchString && !requiredOnly ? 'text-emerald-100 bg-slate-700' : ''"
                    @click="resetFilters"
                />
                <Chip
                    v-for="profile in props.projectProfiles.list()"
                    :label="profile.getDisplayLabel()"
                    class="h-4 !rounded py-3 text-sm border cursor-pointer select-none"
                    :class="profileFilter.includes(profile.getId()) ? 'bg-emerald-50 border-emerald-600 text-slate-700' : ''"
                    @click="
                        profileFilter.includes(profile.getId())
                            ? (profileFilter = profileFilter.filter((e) => e !== profile.getId()))
                            : profileFilter.push(profile.getId())
                    "
                />
            </span>
            <div class="italic flex-grow text-center" :class="{ invisible: !searchString }">
                {{ matchesCount > 0 ? matchesCount : "No " }} match{{ matchesCount != 1 ? `es` : "" }} for
                <span class="font-bold">{{ searchString }}</span>
            </div>
            <span v-if="props.projectProfiles.list().length > 1" class="flex justify-self-end gap-4" grid>
                <span class="flex gap-2" title="Hide optional properties." aria-label="Hide optional properties.">
                    <label for="required">Required only</label>
                    <InputSwitch v-model="requiredOnly" inputId="required" />
                </span>
                <!-- TODO                    <span class="flex gap-2" title="Show all missing properties." aria-label="Show all missing properties.">
                        <label for="missing">Missing only</label>
                        <InputSwitch v-model="missingOnly" inputId="missing" />
                    </span> -->
            </span>
        </div>
    </div>
</template>
