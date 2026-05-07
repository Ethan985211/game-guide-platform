import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../pages/Home.vue')
  },
  {
    path: '/games',
    name: 'Games',
    component: () => import('../pages/Games.vue')
  },
  {
    path: '/games/:id',
    name: 'GameDetail',
    component: () => import('../pages/GameDetail.vue')
  },
  {
    path: '/articles',
    name: 'Articles',
    component: () => import('../pages/Articles.vue')
  },
  {
    path: '/articles/:id',
    name: 'ArticleDetail',
    component: () => import('../pages/ArticleDetail.vue')
  },
  {
    path: '/articles/create',
    name: 'CreateArticle',
    component: () => import('../pages/CreateArticle.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../pages/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../pages/Register.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../pages/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/my-articles',
    name: 'MyArticles',
    component: () => import('../pages/MyArticles.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
