import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LoginComponent from '@/components/LoginComponent.vue';
import WhoamiView from '@/views/WhoamiView.vue';
import { useTokenStore } from '@/store/tokenStore';
import TokenView from '@/views/TokenView.vue';

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/login', name: 'login', component: LoginComponent },
  { path: '/whoami', name: 'whoami', component: WhoamiView, meta: { requiresAuth: true } },
  { path: '/token', name: 'token', component: TokenView, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const tokenStore = useTokenStore();
  const isAuthenticated = tokenStore.getToken !== null;
  
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next({ name: 'login' });
  } else {
    next();
  }
});

export default router;
