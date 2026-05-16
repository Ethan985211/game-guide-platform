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
        <div class="page-header">
          <h1 class="page-title">文章管理</h1>
          <div class="filters">
            <el-input
              v-model="searchQuery"
              placeholder="搜索文章标题..."
              clearable
              @clear="fetchArticles"
              @keyup.enter="fetchArticles"
              style="width: 200px;"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-select v-model="categoryFilter" placeholder="分类筛选" clearable style="width: 150px;">
              <el-option label="攻略" value="guide" />
              <el-option label="资讯" value="news" />
              <el-option label="心得" value="tips" />
            </el-select>
            <el-button type="primary" @click="fetchArticles">筛选</el-button>
          </div>
        </div>

        <div class="table-container">
          <el-table :data="articles" v-loading="loading" stripe>
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="title" label="标题" min-width="200">
              <template #default="{ row }">
                <strong>{{ row.title }}</strong>
              </template>
            </el-table-column>
            <el-table-column prop="category" label="分类" width="100">
              <template #default="{ row }">
                <el-tag size="small">{{ getCategoryLabel(row.category) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="author_username" label="作者" width="120" />
            <el-table-column label="浏览/点赞" width="120">
              <template #default="{ row }">
                <span class="stats-text">{{ row.views }} / {{ row.likes }}</span>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.is_published ? 'success' : 'info'">
                  {{ row.is_published ? '已发布' : '未发布' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="发布时间" width="120">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button size="small" type="warning" @click="togglePublished(row)">
                  {{ row.is_published ? '下架' : '发布' }}
                </el-button>
                <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAdminStore } from '../../stores/admin'
import {
  DataAnalysis, User, Operation, Document, Connection,
  SwitchButton, Search, Avatar, ChatDotRound
} from '@element-plus/icons-vue'

const router = useRouter()
const adminStore = useAdminStore()

const articles = ref([])
const loading = ref(false)
const searchQuery = ref('')
const categoryFilter = ref('')

onMounted(async () => {
  if (!adminStore.isLoggedIn) {
    router.push('/admin/login')
    return
  }
  await fetchArticles()
})

const fetchArticles = async () => {
  loading.value = true
  try {
    articles.value = await adminStore.fetchArticles({
      search: searchQuery.value || undefined,
      category: categoryFilter.value || undefined
    })
  } catch (err) {
    ElMessage.error('获取文章列表失败')
    if (err.response?.status === 401) {
      adminStore.logout()
      router.push('/admin/login')
    }
  } finally {
    loading.value = false
  }
}

const getCategoryLabel = (category) => {
  const labels = {
    guide: '攻略',
    news: '资讯',
    tips: '心得'
  }
  return labels[category] || category
}

const togglePublished = async (article) => {
  try {
    await adminStore.toggleArticlePublished(article.id)
    ElMessage.success(article.is_published ? '文章已下架' : '文章已发布')
    fetchArticles()
  } catch (err) {
    ElMessage.error('操作失败')
  }
}

const handleDelete = async (article) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除文章「${article.title}」吗？此操作不可恢复。`,
      '警告',
      { type: 'warning' }
    )
    await adminStore.deleteArticle(article.id)
    ElMessage.success('文章已删除')
    fetchArticles()
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

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

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
}

.filters {
  display: flex;
  gap: 12px;
  align-items: center;
}

.table-container {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.stats-text {
  color: #666;
  font-size: 13px;
}
</style>
