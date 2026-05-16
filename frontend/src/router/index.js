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
    path: '/login',
    name: 'Login',
    component: () => import('../pages/Login.vue'),
    meta: { disabled: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../pages/Register.vue'),
    meta: { disabled: true }
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
  },
  // 管理员后台
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('../pages/admin/AdminLogin.vue')
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('../pages/admin/AdminDashboard.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: () => import('../pages/admin/AdminUsers.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/games',
    name: 'AdminGames',
    component: () => import('../pages/admin/AdminGames.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/characters',
    name: 'AdminCharacters',
    component: () => import('../pages/admin/AdminCharacters.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/articles',
    name: 'AdminArticles',
    component: () => import('../pages/admin/AdminArticles.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/openclaw',
    name: 'AdminOpenClaw',
    component: () => import('../pages/admin/AdminOpenClaw.vue'),
    meta: { requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  // 检查用户功能是否已禁用
  if (to.meta.disabled) {
    next('/')
    return
  }

  // 检查管理员权限
  if (to.meta.requiresAdmin) {
    const adminToken = localStorage.getItem('admin_token')
    if (!adminToken) {
      next('/admin/login')
      return
    }
  }

  // 检查用户认证
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/')
    return
  }

  next()
})

export default router
