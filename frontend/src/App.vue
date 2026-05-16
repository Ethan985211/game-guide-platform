<template>
  <div id="app">
    <!-- 优化后的导航栏 -->
    <header class="navbar">
      <!-- 左侧 Logo -->
      <div class="nav-left">
        <span class="brand-text">Game<span class="brand-hub">Hub</span></span>
      </div>
      
      <!-- 居中导航 -->
      <nav class="nav-center">
        <router-link to="/">首页</router-link>
        <router-link to="/games">游戏库</router-link>
        <router-link to="/articles">攻略</router-link>
      </nav>
      
      <!-- 右侧 -->
      <div class="nav-right">
      </div>
    </header>

    <main class="main-content">
      <router-view />
    </main>

    <footer class="footer">
      <div class="footer-content">
        <div class="footer-brand">
          <span>GameHub</span>
        </div>
        <div class="footer-links">
          <span>© 2024-2026</span>
          <span>·</span>
          <span>发现精彩游戏</span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { trackPageView } from './utils/analytics'

const router = useRouter()

// 路由变化时追踪页面
router.afterEach((to) => {
  let contentType = 'home'
  let contentId = null
  
  if (to.path.startsWith('/games/')) {
    contentType = 'game'
    contentId = to.params.id ? parseInt(to.params.id) : null
  } else if (to.path.startsWith('/articles/')) {
    contentType = 'article'
    contentId = to.params.id ? parseInt(to.params.id) : null
  } else if (to.path === '/games') {
    contentType = 'games'
  } else if (to.path === '/articles') {
    contentType = 'articles'
  }
  
  trackPageView(contentType, contentId)
})
</script>

<style scoped>
/* 导航栏布局 */
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

/* 左侧品牌 */
.nav-left {
  flex: 1;
}

.brand-text {
  font-size: 22px;
  font-weight: 900;
  letter-spacing: -1px;
  color: var(--text-primary);
}

.brand-hub {
  color: var(--accent);
}

/* 居中导航 */
.nav-center {
  display: flex;
  gap: 32px;
}

.nav-center a {
  text-decoration: none;
  color: var(--text-secondary);
  font-size: 15px;
  font-weight: 600;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.25s;
  position: relative;
}

.nav-center a:hover,
.nav-center a.active {
  color: var(--text-primary);
  background: var(--bg-secondary);
}

.nav-center a::after {
  content: '';
  position: absolute;
  bottom: 4px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 2px;
  background: var(--accent);
  border-radius: 2px;
  transition: width 0.3s;
}

.nav-center a:hover::after,
.nav-center a.active::after {
  width: calc(100% - 32px);
}

/* 右侧登录 */
.nav-right {
  flex: 1;
  display: flex;
  justify-content: flex-end;
}

/* 用户信息 */
.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 10px;
  transition: background 0.2s;
}

.user-info:hover {
  background: var(--bg-secondary);
}

.username {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 14px;
}

/* 登录按钮 */
.btn-login {
  background: var(--accent) !important;
  border-color: var(--accent) !important;
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(255, 107, 0, 0.25);
}

.btn-login:hover {
  background: var(--accent-hover) !important;
  border-color: var(--accent-hover) !important;
  box-shadow: 0 4px 12px rgba(255, 107, 0, 0.35);
  transform: translateY(-1px);
}

/* 管理员入口 */
.admin-link {
  text-decoration: none;
}

.admin-link .el-button {
  font-weight: 600;
}

/* 主要内容区 */
.main-content {
  min-height: calc(100vh - 64px - 80px);
  padding-top: 64px;
}

/* 页脚 */
.footer {
  background: var(--bg-dark);
  color: white;
  padding: 40px 48px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 700;
  font-size: 16px;
}

.footer-logo {
  font-size: 28px;
}

.footer-links {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text-muted);
  font-size: 14px;
}

@media (max-width: 768px) {
  .nav-center {
    gap: 16px;
  }
  
  .nav-center a {
    font-size: 14px;
    padding: 8px 12px;
  }
  
  .footer {
    padding: 32px 20px;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
}
</style>
