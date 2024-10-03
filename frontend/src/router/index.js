import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import HelloWorld2 from '@/components/HelloWorld2.vue'
import LoginComponent from '@/components/LoginComponent.vue'
import WhoamiView from '@/views/WhoamiView.vue'
import TokenView from '@/views/TokenView.vue'
import store from '@/store'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginComponent,
  },
  {
    path: '/whoami',
    name: 'whoami',
    component: WhoamiView,
    meta: {requiresAuth:true}
  },
  {
    path: '/token',
    name: 'token',
    component: TokenView,
    meta: {requiresAuth:true}
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/hello',
    name: 'hello',
    component: HelloWorld2
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  console.log('store:', store.state); // Log the entire state to see if token is being set
  const isAuthenticated = store.getters['token'] !== null; // Use namespaced getter
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
      next({ name: 'login' }); // Redirect to login if not authenticated
  } else {
      next(); // Proceed to the route
  }
});



export default router
