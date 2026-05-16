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
        <div class="page-header">
          <h1 class="page-title">角色管理</h1>
          <div class="header-actions">
            <el-select v-model="selectedGame" placeholder="筛选游戏" clearable style="width: 200px" @change="fetchCharacters">
              <el-option
                v-for="game in games"
                :key="game.id"
                :label="game.name"
                :value="game.id"
              />
            </el-select>
            <el-input
              v-model="searchKeyword"
              placeholder="搜索角色名称..."
              clearable
              style="width: 200px"
              @clear="fetchCharacters"
              @keyup.enter="searchCharacters"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-button type="primary" @click="showAddDialog">添加角色</el-button>
          </div>
        </div>

        <!-- 角色统计 -->
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
              <el-icon><Avatar /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ totalCharacters }}</span>
              <span class="stat-label">角色总数</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%)">
              <el-icon><Monitor /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ totalGames }}</span>
              <span class="stat-label">涉及游戏</span>
            </div>
          </div>
        </div>

        <!-- 角色列表 -->
        <div class="table-card">
          <el-table :data="characters" v-loading="loading" stripe>
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column label="角色" min-width="200">
              <template #default="{ row }">
                <div class="character-info">
                  <el-avatar :size="48" :src="row.image" style="background: var(--gradient-primary)">
                    {{ row.name?.[0] }}
                  </el-avatar>
                  <div class="character-details">
                    <span class="character-name">{{ row.name }}</span>
                    <span class="character-desc">{{ row.description?.slice(0, 50) }}...</span>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="所属游戏" width="150">
              <template #default="{ row }">
                <router-link v-if="row.game" :to="`/games/${row.game.slug}`" class="game-link">
                  {{ row.game?.name }}
                </router-link>
                <span v-else class="text-muted">未关联</span>
              </template>
            </el-table-column>
            <el-table-column label="稀有度" width="100">
              <template #default="{ row }">
                <el-tag v-if="row.rarity" :type="getRarityType(row.rarity)">{{ row.rarity }}</el-tag>
                <span v-else class="text-muted">-</span>
              </template>
            </el-table-column>
            <el-table-column label="元素" width="100">
              <template #default="{ row }">
                <el-tag v-if="row.element" size="small" type="warning">{{ row.element }}</el-tag>
                <span v-else class="text-muted">-</span>
              </template>
            </el-table-column>
            <el-table-column label="武器类型" width="100">
              <template #default="{ row }">
                <el-tag v-if="row.weapon_type" size="small">{{ row.weapon_type }}</el-tag>
                <span v-else class="text-muted">-</span>
              </template>
            </el-table-column>
            <el-table-column label="创建时间" width="120">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button size="small" type="primary" @click="showEditDialog(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="handleDelete(row.id)" :loading="deletingId === row.id">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :total="totalCharacters"
              :page-sizes="[10, 20, 50, 100]"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleSizeChange"
              @current-change="handlePageChange"
            />
          </div>
        </div>
      </div>
    </main>

    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogMode === 'add' ? '添加角色' : '编辑角色'"
      width="600px"
    >
      <el-form :model="form" label-position="top">
        <el-form-item label="角色名称" required>
          <el-input v-model="form.name" placeholder="输入角色名称" />
        </el-form-item>
        <el-form-item label="所属游戏" required>
          <el-select v-model="form.game_id" placeholder="选择游戏" style="width: 100%">
            <el-option
              v-for="game in games"
              :key="game.id"
              :label="game.name"
              :value="game.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="稀有度">
          <el-select v-model="form.rarity" placeholder="选择稀有度" style="width: 100%">
            <el-option label="N (普通)" value="N" />
            <el-option label="R (稀有)" value="R" />
            <el-option label="SR (超稀有)" value="SR" />
            <el-option label="SSR (超级稀有)" value="SSR" />
            <el-option label="UR (终极稀有)" value="UR" />
          </el-select>
        </el-form-item>
        <el-form-item label="元素属性">
          <el-select v-model="form.element" placeholder="选择元素" style="width: 100%">
            <el-option label="火" value="火" />
            <el-option label="水" value="水" />
            <el-option label="雷" value="雷" />
            <el-option label="风" value="风" />
            <el-option label="草" value="草" />
            <el-option label="冰" value="冰" />
            <el-option label="岩" value="岩" />
          </el-select>
        </el-form-item>
        <el-form-item label="武器类型">
          <el-select v-model="form.weapon_type" placeholder="选择武器类型" style="width: 100%">
            <el-option label="单手剑" value="单手剑" />
            <el-option label="双手剑" value="双手剑" />
            <el-option label="长柄武器" value="长柄武器" />
            <el-option label="弓" value="弓" />
            <el-option label="法器" value="法器" />
            <el-option label="双手杖" value="双手杖" />
            <el-option label="拳套" value="拳套" />
          </el-select>
        </el-form-item>
        <el-form-item label="角色描述">
          <el-input v-model="form.description" type="textarea" :rows="4" placeholder="输入角色描述" />
        </el-form-item>
        <el-form-item label="角色图片URL">
          <el-input v-model="form.image" placeholder="输入图片URL" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          {{ dialogMode === 'add' ? '添加' : '保存' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAdminStore } from '../../stores/admin'
import api from '../../api'
import {
  DataAnalysis, UserFilled, Monitor, Document, Connection,
  SwitchButton, ChatDotRound, Avatar, Search
} from '@element-plus/icons-vue'

const router = useRouter()
const adminStore = useAdminStore()

const loading = ref(false)
const submitting = ref(false)
const deletingId = ref(null)
const characters = ref([])
const games = ref([])
const totalCharacters = ref(0)
const totalGames = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const searchKeyword = ref('')
const selectedGame = ref(null)

const dialogVisible = ref(false)
const dialogMode = ref('add')
const form = reactive({
  id: null,
  name: '',
  game_id: null,
  rarity: '',
  element: '',
  weapon_type: '',
  description: '',
  image: ''
})

const fetchCharacters = async () => {
  loading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
      ...(searchKeyword.value && { search: searchKeyword.value }),
      ...(selectedGame.value && { game_id: selectedGame.value })
    }
    
    const response = await api.get('/characters', { params })
    characters.value = response.data || []
    totalCharacters.value = response.data?.length || 0
  } catch (err) {
    console.error('获取角色列表失败:', err)
    ElMessage.error('获取角色列表失败')
  } finally {
    loading.value = false
  }
}

const fetchGames = async () => {
  try {
    const response = await api.get('/games', { params: { limit: 100 } })
    games.value = response.data || []
    totalGames.value = games.value.length
  } catch (err) {
    console.error('获取游戏列表失败:', err)
  }
}

const searchCharacters = () => {
  currentPage.value = 1
  fetchCharacters()
}

const showAddDialog = () => {
  dialogMode.value = 'add'
  Object.assign(form, {
    id: null,
    name: '',
    game_id: null,
    rarity: '',
    element: '',
    weapon_type: '',
    description: '',
    image: ''
  })
  dialogVisible.value = true
}

const showEditDialog = (character) => {
  dialogMode.value = 'edit'
  Object.assign(form, {
    id: character.id,
    name: character.name,
    game_id: character.game_id,
    rarity: character.rarity || '',
    element: character.element || '',
    weapon_type: character.weapon_type || '',
    description: character.description || '',
    image: character.image || ''
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!form.name) {
    ElMessage.warning('请输入角色名称')
    return
  }
  if (!form.game_id) {
    ElMessage.warning('请选择所属游戏')
    return
  }
  
  submitting.value = true
  try {
    if (dialogMode.value === 'add') {
      await api.post('/characters', form, {
        headers: { 'X-Admin-Token': adminStore.token }
      })
      ElMessage.success('添加成功')
    } else {
      await api.put(`/characters/${form.id}`, form, {
        headers: { 'X-Admin-Token': adminStore.token }
      })
      ElMessage.success('保存成功')
    }
    dialogVisible.value = false
    fetchCharacters()
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '操作失败')
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个角色吗？删除后无法恢复。',
      '删除确认',
      {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )
    
    deletingId.value = id
    await api.delete(`/characters/${id}`, {
      headers: { 'X-Admin-Token': adminStore.token }
    })
    
    ElMessage.success('删除成功')
    fetchCharacters()
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('删除失败')
    }
  } finally {
    deletingId.value = null
  }
}

const handleSizeChange = () => {
  currentPage.value = 1
  fetchCharacters()
}

const handlePageChange = () => {
  fetchCharacters()
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

const getRarityType = (rarity) => {
  const types = {
    'N': 'info',
    'R': '',
    'SR': 'warning',
    'SSR': 'danger',
    'UR': 'success'
  }
  return types[rarity] || 'info'
}

const handleLogout = () => {
  adminStore.logout()
  ElMessage.success('已退出登录')
  router.push('/admin/login')
}

onMounted(() => {
  if (!adminStore.isLoggedIn) {
    router.push('/admin/login')
    return
  }
  fetchCharacters()
  fetchGames()
})
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
  max-width: 1400px;
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

.header-actions {
  display: flex;
  gap: 12px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 24px;
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

.table-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.character-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.character-details {
  display: flex;
  flex-direction: column;
}

.character-name {
  font-weight: 600;
  color: #333;
}

.character-desc {
  font-size: 12px;
  color: #999;
}

.game-link {
  color: var(--accent);
  text-decoration: none;
}

.game-link:hover {
  text-decoration: underline;
}

.text-muted {
  color: #999;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
