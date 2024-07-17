<script setup lang="ts">
import Card from "primevue/card";
import ScrollPanel from "primevue/scrollpanel";
import Timeline from "primevue/timeline";
import { type PropType, ref, toRefs } from "vue";

import { Project } from "@common/data/entities/project/Project";

const props = defineProps({
    project: {
        type: Object as PropType<Project>,
        required: true,
    },
});
const { project } = toRefs(props);

const events = ref([
    { status: "Ordered", date: "15/10/2020 10:30", icon: "pi pi-shopping-cart", color: "#9C27B0" },
    { status: "Processing", date: "15/10/2020 14:00", icon: "pi pi-cog", color: "#673AB7" },
    { status: "Shipped", date: "15/10/2020 16:15", icon: "pi pi-shopping-cart", color: "#FF9800" },
    { status: "Delivered", date: "16/10/2020 10:00", icon: "pi pi-check", color: "#607D8B" },
]);
</script>

<template>
    <ScrollPanel class="w-full h-full">
        <Timeline :value="events" align="alternate">
            <template #marker="slotProps">
                <span class="flex w-8 h-8 items-center justify-center text-white rounded-full z-1 shadow-1" :style="{ backgroundColor: slotProps.item.color }">
                    <i :class="slotProps.item.icon"></i>
                </span>
            </template>
            <template #content="slotProps">
                <Card class="mt-3">
                    <template #title>
                        {{ slotProps.item.status }}
                    </template>
                    <template #subtitle>
                        {{ slotProps.item.date }}
                    </template>
                    <template #content>
                        <img
                            v-if="slotProps.item.image"
                            :src="`https://primefaces.org/cdn/primevue/images/product/${slotProps.item.image}`"
                            :alt="slotProps.item.name"
                            width="200"
                            class="shadow-1"
                        />
                        <p>
                            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Inventore sed consequuntur error repudiandae numquam deserunt quisquam
                            repellat libero asperiores earum nam nobis, culpa ratione quam perferendis esse, cupiditate neque quas!
                        </p>
                        <Button label="Read more" text></Button>
                    </template>
                </Card>
            </template>
        </Timeline>
    </ScrollPanel>
</template>

<style scoped lang="scss"></style>
