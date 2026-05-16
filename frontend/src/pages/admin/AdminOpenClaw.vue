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
          <el-icon><User /></el-icon>
          用户管理
        </router-link>
        <router-link to="/admin/games" active-class="active">
          <el-icon><Operation /></el-icon>
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
        <h1 class="page-title">Hermes Agent 智能体</h1>

        <!-- 状态卡片 -->
        <div class="status-card">
          <div class="status-header">
            <div class="status-indicator online"></div>
            <span class="status-text">服务在线</span>
          </div>
          <div class="status-info">
            <p>Game Guide Platform — Hermes Agent</p>
            <p class="version">Version 2.0.0</p>
          </div>
        </div>

        <!-- API配置 -->
        <div class="config-section">
          <h2>API 配置</h2>
          <div class="config-card">
            <div class="config-item">
              <label>API 端点</label>
              <code>{{ apiBaseUrl }}/hermes</code>
            </div>
            <div class="config-item">
              <label>API 密钥</label>
              <div class="api-key-display">
                <code v-if="showKey">{{ apiKey }}</code>
                <code v-else>••••••••••••••••</code>
                <el-button size="small" @click="showKey = !showKey">
                  {{ showKey ? '隐藏' : '显示' }}
                </el-button>
              </div>
            </div>
          </div>
        </div>

        <!-- 可用功能 -->
        <div class="features-section">
          <h2>可用功能</h2>
          <div class="features-grid">
            <div class="feature-card">
              <el-icon class="feature-icon"><Search /></el-icon>
              <h3>搜索游戏</h3>
              <p>GET /hermes/games/search?q={keyword}</p>
            </div>
            <div class="feature-card">
              <el-icon class="feature-icon"><InfoFilled /></el-icon>
              <h3>游戏详情</h3>
              <p>GET /hermes/games/{id}</p>
            </div>
            <div class="feature-card">
              <el-icon class="feature-icon"><User /></el-icon>
              <h3>游戏角色</h3>
              <p>GET /hermes/games/{id}/characters</p>
            </div>
            <div class="feature-card">
              <el-icon class="feature-icon"><Document /></el-icon>
              <h3>搜索文章</h3>
              <p>GET /hermes/articles/search?q={keyword}</p>
            </div>
            <div class="feature-card">
              <el-icon class="feature-icon"><Reading /></el-icon>
              <h3>文章详情</h3>
              <p>GET /hermes/articles/{id}</p>
            </div>
            <div class="feature-card">
              <el-icon class="feature-icon"><ChatLineSquare /></el-icon>
              <h3>发表评论</h3>
              <p>POST /hermes/comments</p>
            </div>
            <div class="feature-card">
              <el-icon class="feature-icon"><DataAnalysis /></el-icon>
              <h3>平台统计</h3>
              <p>GET /hermes/stats</p>
            </div>
            <div class="feature-card">
              <el-icon class="feature-icon"><Cpu /></el-icon>
              <h3>AI查询</h3>
              <p>POST /hermes/query</p>
            </div>
          </div>
        </div>

        <!-- 使用示例 -->
        <div class="example-section">
          <h2>使用示例</h2>
          <div class="example-card">
            <h3>cURL 示例</h3>
            <pre class="code-block">curl -X GET "{{ apiBaseUrl }}/hermes/games/search?q=原神" \
  -H "X-API-Key: {{ apiKey }}"</pre>
          </div>
          <div class="example-card">
            <h3>JavaScript 示例</h3>
            <pre class="code-block">const response = await fetch('{{ apiBaseUrl }}/hermes/stats', {
  headers: {
    'X-API-Key': '{{ apiKey }}'
  }
});
const data = await response.json();</pre>
          </div>
        </div>

        <!-- 注意事项 -->
        <div class="notice-section">
          <el-alert
            title="使用提示"
            type="info"
            :closable="false"
          >
            <template #default>
              <ul>
                <li>所有API请求都需要在Header中包含 <code>X-API-Key</code> 字段</li>
                <li>API密钥请妥善保管，不要泄露给未经授权的用户</li>
                <li>发表评论功能会以系统管理员身份发表</li>
                <li>如需修改API密钥，请编辑后端 .env 文件</li>
              </ul>
            </template>
          </el-alert>
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
  DataAnalysis, User, Operation, Document, Connection,
  SwitchButton, Search, InfoFilled, Reading, ChatLineSquare, Cpu,
  Avatar, ChatDotRound
} from '@element-plus/icons-vue'

const router = useRouter()
const adminStore = useAdminStore()

const showKey = ref(false)
const apiBaseUrl = ref(window.location.origin + '/api')
const apiKey = ref('')

onMounted(() => {
  if (!adminStore.isLoggedIn) {
    router.push('/admin/login')
    return
  }
  // 从本地存储获取（实际使用时应该从后端获取）
  apiKey.value = 'hm-agent-key-gqp-2026'
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
  max-width: 900px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 24px;
}

.status-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.status-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #909399;
}

.status-indicator.online {
  background: #67c23a;
  box-shadow: 0 0 8px rgba(103, 194, 58, 0.6);
}

.status-text {
  font-weight: 600;
  color: #67c23a;
}

.status-info p {
  margin: 0;
  color: #666;
}

.version {
  color: #999 !important;
  font-size: 13px;
  margin-top: 4px !important;
}

.config-section,
.features-section,
.example-section,
.notice-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.config-section h2,
.features-section h2,
.example-section h2 {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 20px;
}

.config-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
}

.config-item {
  margin-bottom: 16px;
}

.config-item:last-child {
  margin-bottom: 0;
}

.config-item label {
  display: block;
  font-size: 13px;
  color: #666;
  margin-bottom: 6px;
}

.config-item code {
  background: #e9e9e9;
  padding: 6px 10px;
  border-radius: 4px;
  font-size: 13px;
  color: #333;
  word-break: break-all;
}

.api-key-display {
  display: flex;
  align-items: center;
  gap: 12px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.feature-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
}

.feature-icon {
  font-size: 32px;
  color: #ff8c00;
  margin-bottom: 8px;
}

.feature-card h3 {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 8px;
}

.feature-card p {
  font-size: 12px;
  color: #666;
  margin: 0;
  word-break: break-all;
}

.example-card {
  background: #1e1e1e;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}

.example-card:last-child {
  margin-bottom: 0;
}

.example-card h3 {
  color: #fff;
  font-size: 14px;
  margin-bottom: 12px;
}

.code-block {
  background: #2d2d2d;
  padding: 12px;
  border-radius: 4px;
  margin: 0;
  overflow-x: auto;
  font-size: 13px;
  line-height: 1.5;
  color: #d4d4d4;
}

.notice-section ul {
  margin: 0;
  padding-left: 20px;
}

.notice-section li {
  margin-bottom: 8px;
  line-height: 1.6;
}

.notice-section code {
  background: #e9e9e9;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
}
</style>
