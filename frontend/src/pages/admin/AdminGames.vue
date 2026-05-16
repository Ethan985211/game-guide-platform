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
          <h1 class="page-title">游戏管理</h1>
          <el-button type="primary" @click="showAddDialog">
            <el-icon><Plus /></el-icon>
            添加游戏
          </el-button>
        </div>

        <div class="table-container">
          <el-table :data="games" v-loading="loading" stripe>
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column label="封面" width="100">
              <template #default="{ row }">
                <el-avatar v-if="row.cover_image" :src="row.cover_image" :size="50" shape="square" />
                <div v-else class="no-cover">无</div>
              </template>
            </el-table-column>
            <el-table-column prop="name" label="游戏名称" min-width="150">
              <template #default="{ row }">
                <strong>{{ row.name }}</strong>
              </template>
            </el-table-column>
            <el-table-column prop="category" label="分类" width="100">
              <template #default="{ row }">
                <el-tag size="small">{{ row.category }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="developer" label="开发商" min-width="120" />
            <el-table-column prop="created_at" label="添加时间" width="120">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="160" fixed="right">
              <template #default="{ row }">
                <el-button size="small" type="primary" @click="showEditDialog(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </main>

    <!-- 添加/编辑游戏对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑游戏' : '添加游戏'"
      width="600px"
    >
      <el-form :model="gameForm" label-width="100px">
        <el-form-item label="游戏名称">
          <el-input v-model="gameForm.name" placeholder="请输入游戏名称" />
        </el-form-item>
        <el-form-item label="URL别名">
          <el-input v-model="gameForm.slug" placeholder="URL-friendly名称，如：genshin-impact" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="gameForm.category" placeholder="请选择分类">
            <el-option label="RPG" value="RPG" />
            <el-option label="FPS" value="FPS" />
            <el-option label="MOBA" value="MOBA" />
            <el-option label="SLG" value="SLG" />
            <el-option label="休闲" value="Casual" />
            <el-option label="其他" value="Other" />
          </el-select>
        </el-form-item>
        <el-form-item label="开发商">
          <el-input v-model="gameForm.developer" placeholder="请输入开发商" />
        </el-form-item>
        <el-form-item label="发行商">
          <el-input v-model="gameForm.publisher" placeholder="请输入发行商" />
        </el-form-item>
        <el-form-item label="封面图URL">
          <el-input v-model="gameForm.cover_image" placeholder="请输入封面图URL" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="gameForm.description"
            type="textarea"
            :rows="4"
            placeholder="请输入游戏描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          {{ isEdit ? '保存' : '添加' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAdminStore } from '../../stores/admin'
import {
  DataAnalysis, User, Operation, Document, Connection,
  SwitchButton, Plus, Avatar, ChatDotRound
} from '@element-plus/icons-vue'

const router = useRouter()
const adminStore = useAdminStore()

const games = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const editingId = ref(null)

const gameForm = ref({
  name: '',
  slug: '',
  category: 'RPG',
  developer: '',
  publisher: '',
  cover_image: '',
  description: ''
})

onMounted(async () => {
  if (!adminStore.isLoggedIn) {
    router.push('/admin/login')
    return
  }
  await fetchGames()
})

const fetchGames = async () => {
  loading.value = true
  try {
    games.value = await adminStore.fetchGames()
  } catch (err) {
    ElMessage.error('获取游戏列表失败')
    if (err.response?.status === 401) {
      adminStore.logout()
      router.push('/admin/login')
    }
  } finally {
    loading.value = false
  }
}

const showAddDialog = () => {
  isEdit.value = false
  editingId.value = null
  gameForm.value = {
    name: '',
    slug: '',
    category: 'RPG',
    developer: '',
    publisher: '',
    cover_image: '',
    description: ''
  }
  dialogVisible.value = true
}

const showEditDialog = (game) => {
  isEdit.value = true
  editingId.value = game.id
  gameForm.value = { ...game }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  submitting.value = true
  try {
    if (isEdit.value) {
      await adminStore.updateGame(editingId.value, gameForm.value)
      ElMessage.success('游戏更新成功')
    } else {
      await adminStore.createGame(gameForm.value)
      ElMessage.success('游戏添加成功')
    }
    dialogVisible.value = false
    fetchGames()
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '操作失败')
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (game) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除游戏「${game.name}」吗？此操作将同时删除关联的角色和文章。`,
      '警告',
      { type: 'warning' }
    )
    await adminStore.deleteGame(game.id)
    ElMessage.success('游戏已删除')
    fetchGames()
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

.table-container {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.no-cover {
  width: 50px;
  height: 50px;
  background: #f0f0f0;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 12px;
}
</style>
