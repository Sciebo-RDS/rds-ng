declare module "*.vue" {
    import Vue from "vue";
    import { defineComponent } from 'vue';

    const component: ReturnType<typeof defineComponent>;
    export default component;
}

declare module ".ts" {
    import pinia from "pinia";
    export default pinia;
}
