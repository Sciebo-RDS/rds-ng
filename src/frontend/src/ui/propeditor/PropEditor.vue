<script setup lang="ts">
import { provide } from "vue";
import PropCategory from "./PropCategory.vue";

const props = defineProps(["controller"]);

provide("controller", props.controller);
</script>

<template>
    <div>
        <div v-for="profileId in props.controller.getProfileIds()">
            <div class="text-2xl bg-sky-100">
                {{ `${profileId[0]} v${profileId[1]}` }}
            </div>
            <div class="">
                <PropCategory
                    v-for="category in props.controller.getCategoryById(
                        profileId
                    )"
                    :category="category"
                    :profileId="profileId"
                    class="my-5"
                />
            </div>
        </div>
    </div>
</template>
