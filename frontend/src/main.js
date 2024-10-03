import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import PrimeVue from 'primevue/config';
import store from './store';
import './assets/tailwind.css';


const app = createApp(App).use(router).use(store).use(PrimeVue)

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://127.0.0.1:8000/';  // the FastAPI backend


// Axios request interceptor to add token to headers
axios.interceptors.request.use(
    config => {
        const token = store.getters.token; // Access the token from Vuex store
        if (token) {
            config.headers['Authorization'] = token; // Add token to Authorization header
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);


axios.interceptors.response.use(
    response => {
        return response;
    },
    error => {
        if (error.response.status === 401) {
            // Token is invalid or expired, redirect to login page
            store.commit('clearToken'); // Clear token from Vuex
            router.push('/login'); // Redirect to login
        }
        return Promise.reject(error);
    }
);

app.config.globalProperties.$axios = axios



app.mount('#app')
