import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import axios from 'axios';
import './assets/tailwind.css';

const pinia = createPinia();
const app = createApp(App);

app.use(router).use(pinia);
axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://127.0.0.1:8000/';

app.mount('#app');
