import { defineStore } from "pinia";
import { ref } from "vue";

export const networkStore = defineStore("networkStore", () => {
    const connected = ref(false);

    return { connected };
});
