import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';                 // Icons


const app = createApp(App).use(router).use(PrimeVue, {
    theme: {
        preset: Aura
    }
})

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://127.0.0.1:8000/';  // the FastAPI backend

app.config.globalProperties.$axios = axios



app.mount('#app')
