import '@common/assets/styles/tailwind-init.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import PrimeVue from 'primevue/config'

import App from './App.vue'
import Button from "primevue/button"
import "primevue/resources/themes/lara-light-indigo/theme.css"

const app = createApp(App)

app.use(createPinia())

app.use(PrimeVue)

app.component('Button', Button);

app.mount('#app')
