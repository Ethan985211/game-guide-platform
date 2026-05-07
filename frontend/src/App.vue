<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <router-link to="/" class="logo">
            <span class="logo-icon">🎮</span>
            <span>游戏攻略</span>
          </router-link>
          <div class="nav-links">
            <router-link to="/">首页</router-link>
            <router-link to="/games">游戏库</router-link>
            <router-link to="/articles">攻略文章</router-link>
          </div>
          <div class="user-area">
            <template v-if="authStore.isLoggedIn">
              <el-dropdown @command="handleCommand">
                <span class="user-info">
                  <el-avatar :src="authStore.user?.avatar" :size="32">
                    {{ authStore.user?.username?.[0] }}
                  </el-avatar>
                  <span>{{ authStore.user?.username }}</span>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                    <el-dropdown-item command="my-articles">我的文章</el-dropdown-item>
                    <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </template>
            <template v-else>
              <router-link to="/login">
                <el-button type="primary" size="small">登录</el-button>
              </router-link>
            </template>
          </div>
        </div>
      </el-header>

      <el-main>
        <router-view />
      </el-main>

      <el-footer>© 2024 游戏攻略聚合平台</el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleCommand = (command) => {
  if (command === 'logout') {
    authStore.logout()
    router.push('/')
  } else if (command === 'profile') {
    router.push('/profile')
  } else if (command === 'my-articles') {
    router.push('/my-articles')
  }
}
</script>

<style scoped>
.el-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.logo-icon {
  font-size: 28px;
}

.nav-links {
  display: flex;
  gap: 24px;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.3s;
}

.nav-links a:hover {
  opacity: 0.8;
}

.user-area {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  cursor: pointer;
}

.el-main {
  min-height: calc(100vh - 120px);
  background: #f5f7fa;
}

.el-footer {
  text-align: center;
  padding: 20px;
  background: #2c3e50;
  color: #ecf0f1;
}
</style>
