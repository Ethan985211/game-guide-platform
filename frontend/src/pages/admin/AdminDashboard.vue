<template>
  <div class="admin-page">
    <aside class="admin-sidebar">
      <div class="sidebar-header">
        <h2>管理后台</h2>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/admin" exact-active-class="active">
          <el-icon><DataAnalysis /></el-icon>
          仪表盘
        </router-link>
        <router-link to="/admin/users" active-class="active">
          <el-icon><UserFilled /></el-icon>
          用户管理
        </router-link>
        <router-link to="/admin/games" active-class="active">
          <el-icon><Monitor /></el-icon>
          游戏管理
        </router-link>
        <router-link to="/admin/characters" active-class="active">
          <el-icon><Avatar /></el-icon>
          角色管理
        </router-link>
        <router-link to="/admin/articles" active-class="active">
          <el-icon><Document /></el-icon>
          文章管理
        </router-link>
        <router-link to="/admin/hermes" active-class="active">
          <el-icon><Connection /></el-icon>
          Hermes Agent
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <button @click="handleLogout" class="logout-btn">
          <el-icon><SwitchButton /></el-icon>
          退出登录
        </button>
      </div>
    </aside>

    <main class="admin-main">
      <div class="admin-content">
        <h1 class="page-title">仪表盘</h1>

        <!-- 统计卡片 -->
        <div class="stats-grid">
          <div class="stat-card highlight">
            <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
              <el-icon><View /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ stats?.total_views || 0 }}</span>
              <span class="stat-label">总浏览量</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%)">
              <el-icon><Monitor /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ stats?.total_games || 0 }}</span>
              <span class="stat-label">收录游戏</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)">
              <el-icon><Document /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ stats?.total_articles || 0 }}</span>
              <span class="stat-label">攻略文章</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)">
              <el-icon><TrendCharts /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ stats?.today_views || 0 }}</span>
              <span class="stat-label">今日浏览</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)">
              <el-icon><UserFilled /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ stats?.total_users || 0 }}</span>
              <span class="stat-label">注册用户</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%)">
              <el-icon><User /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ stats?.verified_users || 0 }}</span>
              <span class="stat-label">已验证用户</span>
            </div>
          </div>
        </div>

        <!-- 访客统计 -->
        <div class="stats-grid" v-if="analytics">
          <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%)">
              <el-icon><User /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ analytics.unique_visitors || 0 }}</span>
              <span class="stat-label">独立访客</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)">
              <el-icon><Clock /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ analytics.period_views || 0 }}</span>
              <span class="stat-label">{{ analytics.period_days || 7 }}天浏览</span>
            </div>
          </div>
        </div>

        <!-- 近期数据 -->
        <div class="recent-section">
          <h2>近期数据（7天）</h2>
          <div class="recent-grid">
            <div class="recent-card">
              <span class="recent-value">{{ stats?.recent_views || 0 }}</span>
              <span class="recent-label">新增浏览</span>
            </div>
            <div class="recent-card">
              <span class="recent-value">{{ stats?.recent_articles || 0 }}</span>
              <span class="recent-label">新增文章</span>
            </div>
            <div class="recent-card">
              <span class="recent-value">{{ stats?.new_games || 0 }}</span>
              <span class="recent-label">新增游戏</span>
            </div>
            <div class="recent-card">
              <span class="recent-value">{{ stats?.recent_comments || 0 }}</span>
              <span class="recent-label">新增评论</span>
            </div>
          </div>
        </div>

        <!-- 快捷操作 -->
        <div class="quick-actions">
          <h2>快捷操作</h2>
          <div class="action-buttons">
            <router-link to="/admin/users">
              <el-button type="primary" plain>
                <el-icon><DataLine /></el-icon>
                数据统计
              </el-button>
            </router-link>
            <router-link to="/admin/games">
              <el-button type="success" plain>
                <el-icon><Monitor /></el-icon>
                管理游戏
              </el-button>
            </router-link>
            <router-link to="/admin/articles">
              <el-button type="warning" plain>
                <el-icon><Document /></el-icon>
                管理文章
              </el-button>
            </router-link>
            <router-link to="/">
              <el-button type="info" plain>
                <el-icon><View /></el-icon>
                查看前台
              </el-button>
            </router-link>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAdminStore } from '../../stores/admin'
import {
  DataAnalysis, UserFilled, Monitor, Document, Connection,
  SwitchButton, View, TrendCharts, User, Clock, Avatar
} from '@element-plus/icons-vue'

const router = useRouter()
const adminStore = useAdminStore()

const stats = ref(null)
const analytics = ref(null)

onMounted(async () => {
  if (!adminStore.isLoggedIn) {
    router.push('/admin/login')
    return
  }

  // 获取主统计数据
  try {
    stats.value = await adminStore.fetchStats()
  } catch (err) {
    ElMessage.error('获取统计数据失败')
    console.error('Stats error:', err)
    if (err.response?.status === 401) {
      adminStore.logout()
      router.push('/admin/login')
    }
  }

  // 独立获取分析摘要（不阻塞主数据）
  adminStore.fetchAnalyticsSummary().then(data => {
    if (data) {
      analytics.value = data
    }
  }).catch(e => {
    console.warn('获取分析摘要失败(非阻塞):', e)
  })
})

const handleLogout = () => {
  adminStore.logout()
  ElMessage.success('已退出登录')
  router.push('/admin/login')
}
</script>

<style scoped>
.admin-page {
  display: flex;
  min-height: 100vh;
  background: #f5f7fa;
}

.admin-sidebar {
  width: 240px;
  background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
  color: white;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header h2 {
  font-size: 18px;
  font-weight: 700;
  color: #ff8c00;
}

.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
}

.sidebar-nav a {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  border-radius: 10px;
  margin-bottom: 4px;
  transition: all 0.3s;
  font-size: 14px;
}

.sidebar-nav a:hover,
.sidebar-nav a.active {
  background: rgba(255, 140, 0, 0.2);
  color: #ff8c00;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.3s;
}

.logout-btn:hover {
  background: rgba(255, 100, 100, 0.3);
  color: #ff6b6b;
}

.admin-main {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.admin-content {
  max-width: 1200px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 24px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: white;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #1a1a1a;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-top: 4px;
}

.recent-section,
.quick-actions {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.recent-section h2,
.quick-actions h2 {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 20px;
}

.recent-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.recent-card {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
}

.recent-value {
  display: block;
  font-size: 36px;
  font-weight: 700;
  color: #ff8c00;
}

.recent-label {
  display: block;
  font-size: 14px;
  color: #666;
  margin-top: 8px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.action-buttons a {
  text-decoration: none;
}
</style>
