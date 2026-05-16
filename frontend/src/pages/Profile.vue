<template>
  <div class="profile page">
    <div class="page-header">
      <h1 class="page-title">个人设置</h1>
      <p class="page-subtitle">管理你的个人信息和账户安全</p>
    </div>

    <div class="profile-content">
      <!-- 左侧菜单 -->
      <div class="profile-sidebar">
        <div class="user-card">
          <div class="user-avatar-wrapper">
            <el-avatar :size="100" class="user-avatar" :src="previewAvatar">
              {{ authStore.user?.username?.[0] }}
            </el-avatar>
            <div class="avatar-ring"></div>
          </div>
          <h2 class="user-name">{{ authStore.user?.username }}</h2>
          <p class="user-email">{{ authStore.user?.email }}</p>
          <div class="user-stats">
            <div class="stat-item">
              <span class="stat-value">{{ articlesCount }}</span>
              <span class="stat-label">文章</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-value">{{ authStore.user?.is_admin ? '管理员' : '用户' }}</span>
              <span class="stat-label">身份</span>
            </div>
          </div>
          <p class="user-bio">{{ authStore.user?.bio || '这个人很懒，什么都没写' }}</p>
        </div>
        
        <!-- 设置菜单 -->
        <div class="settings-menu">
          <button 
            v-for="item in menuItems" 
            :key="item.key"
            :class="['menu-item', { active: activeTab === item.key }]"
            @click="activeTab = item.key"
          >
            <el-icon><component :is="item.icon" /></el-icon>
            {{ item.label }}
          </button>
        </div>
      </div>

      <!-- 右侧内容 -->
      <div class="profile-main">
        <!-- 基本资料 -->
        <div v-show="activeTab === 'profile'" class="edit-card">
          <div class="card-header">
            <div class="card-title-group">
              <h3 class="card-title">基本资料</h3>
              <p class="card-subtitle">更新你的个人信息</p>
            </div>
          </div>
          <el-form :model="form" label-position="top" class="profile-form">
            <el-form-item label="头像">
              <div class="avatar-upload">
                <el-avatar :size="80" :src="previewAvatar" class="preview-avatar">
                  {{ authStore.user?.username?.[0] }}
                </el-avatar>
                <div class="avatar-actions">
                  <el-button size="small" @click="triggerAvatarInput">
                    <el-icon><Upload /></el-icon>
                    更换头像
                  </el-button>
                  <input 
                    ref="avatarInput" 
                    type="file" 
                    accept="image/*" 
                    style="display: none"
                    @change="handleAvatarChange"
                  />
                  <p class="avatar-tip">支持 JPG、PNG 格式，最大 2MB</p>
                </div>
              </div>
            </el-form-item>
            <el-form-item label="用户名">
              <el-input 
                v-model="form.username" 
                placeholder="输入用户名"
                size="large"
              >
                <template #prefix>
                  <el-icon><User /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item label="个人简介">
              <el-input 
                v-model="form.bio" 
                type="textarea" 
                :rows="4" 
                placeholder="介绍一下自己吧..."
                maxlength="200"
                show-word-limit
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" size="large" @click="saveProfile" :loading="saving">
                <el-icon v-if="!saving"><Check /></el-icon>
                保存修改
              </el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- 安全设置 -->
        <div v-show="activeTab === 'security'" class="edit-card">
          <div class="card-header">
            <div class="card-title-group">
              <h3 class="card-title">账户安全</h3>
              <p class="card-subtitle">管理你的账户安全设置</p>
            </div>
          </div>
          
          <!-- 账户信息 -->
          <div class="security-section">
            <h4 class="section-title">账户信息</h4>
            <div class="security-info">
              <div class="info-row">
                <div class="info-item">
                  <span class="info-label">邮箱</span>
                  <span class="info-value">{{ authStore.user?.email }}</span>
                </div>
                <el-tag type="success" effect="dark" size="small">
                  已验证
                </el-tag>
              </div>
              <div class="info-row">
                <div class="info-item">
                  <span class="info-label">注册时间</span>
                  <span class="info-value">{{ formatDate(authStore.user?.created_at) }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 修改密码 -->
          <div class="security-section">
            <h4 class="section-title">修改密码</h4>
            <el-form :model="passwordForm" label-position="top" class="password-form">
              <el-form-item label="当前密码">
                <el-input 
                  v-model="passwordForm.old_password" 
                  type="password" 
                  placeholder="请输入当前密码"
                  size="large"
                  show-password
                />
              </el-form-item>
              <el-form-item label="新密码">
                <el-input 
                  v-model="passwordForm.new_password" 
                  type="password" 
                  placeholder="请输入新密码（至少6位）"
                  size="large"
                  show-password
                />
              </el-form-item>
              <el-form-item label="确认新密码">
                <el-input 
                  v-model="passwordForm.confirm_password" 
                  type="password" 
                  placeholder="请再次输入新密码"
                  size="large"
                  show-password
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" size="large" @click="changePassword" :loading="changingPassword">
                  修改密码
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>

        <!-- 偏好设置 -->
        <div v-show="activeTab === 'preferences'" class="edit-card">
          <div class="card-header">
            <div class="card-title-group">
              <h3 class="card-title">偏好设置</h3>
              <p class="card-subtitle">自定义你的使用体验</p>
            </div>
          </div>
          
          <div class="preferences-list">
            <div class="preference-item">
              <div class="preference-info">
                <span class="preference-label">邮件通知</span>
                <span class="preference-desc">接收文章更新和评论通知</span>
              </div>
              <el-switch v-model="preferences.emailNotification" />
            </div>
            <div class="preference-item">
              <div class="preference-info">
                <span class="preference-label">公开我的资料</span>
                <span class="preference-desc">允许其他人查看你的个人资料</span>
              </div>
              <el-switch v-model="preferences.publicProfile" />
            </div>
            <div class="preference-item">
              <div class="preference-info">
                <span class="preference-label">显示我的文章数</span>
                <span class="preference-desc">在个人资料中显示发布的文章数量</span>
              </div>
              <el-switch v-model="preferences.showArticleCount" />
            </div>
          </div>
          
          <div class="preferences-actions">
            <el-button type="primary" @click="savePreferences">
              保存偏好设置
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, markRaw } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Check, Upload, Lock, Bell, Setting, Document, Edit } from '@element-plus/icons-vue'
import { useAuthStore } from '../stores/auth'
import { articleAPI } from '../api'
import api from '../api'

const authStore = useAuthStore()

// 状态
const activeTab = ref('profile')
const form = ref({
  username: '',
  bio: '',
  avatar: ''
})
const passwordForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
})
const preferences = ref({
  emailNotification: true,
  publicProfile: true,
  showArticleCount: true
})
const saving = ref(false)
const changingPassword = ref(false)
const articlesCount = ref(0)
const avatarInput = ref(null)
const previewAvatar = ref('')

// 菜单项
const menuItems = [
  { key: 'profile', label: '基本资料', icon: markRaw(Edit) },
  { key: 'security', label: '账户安全', icon: markRaw(Lock) },
  { key: 'preferences', label: '偏好设置', icon: markRaw(Setting) },
]

// 加载文章数量
const loadArticlesCount = async () => {
  try {
    const response = await articleAPI.getArticles({
      author_id: authStore.user?.id,
      limit: 100
    })
    articlesCount.value = response.data?.length || 0
  } catch (error) {
    console.error('获取文章数量失败', error)
  }
}

// 初始化
onMounted(() => {
  form.value.username = authStore.user?.username || ''
  form.value.bio = authStore.user?.bio || ''
  form.value.avatar = authStore.user?.avatar || ''
  previewAvatar.value = authStore.user?.avatar || ''
  loadArticlesCount()
  
  // 加载本地存储的偏好设置
  const savedPrefs = localStorage.getItem('userPreferences')
  if (savedPrefs) {
    preferences.value = { ...preferences.value, ...JSON.parse(savedPrefs) }
  }
})

// 保存基本资料
const saveProfile = async () => {
  if (!form.value.username.trim()) {
    ElMessage.warning('用户名不能为空')
    return
  }
  saving.value = true
  try {
    const response = await api.put('/auth/me', {
      username: form.value.username,
      bio: form.value.bio
    })
    await authStore.fetchUser()
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

// 触发头像选择
const triggerAvatarInput = () => {
  avatarInput.value?.click()
}

// 处理头像选择
const handleAvatarChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  // 验证文件大小 (2MB)
  if (file.size > 2 * 1024 * 1024) {
    ElMessage.error('图片大小不能超过 2MB')
    return
  }
  
  // 验证文件类型
  if (!file.type.startsWith('image/')) {
    ElMessage.error('请选择图片文件')
    return
  }
  
  // 预览头像
  previewAvatar.value = URL.createObjectURL(file)
  
  // 上传头像
  try {
    const formData = new FormData()
    formData.append('avatar', await fileToBase64(file))
    
    await api.post('/auth/upload-avatar', {
      avatar: await fileToBase64(file)
    })
    
    await authStore.fetchUser()
    ElMessage.success('头像上传成功')
  } catch (error) {
    ElMessage.error('头像上传失败')
    previewAvatar.value = authStore.user?.avatar || ''
  }
}

// 文件转 Base64
const fileToBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => resolve(reader.result)
    reader.onerror = (error) => reject(error)
  })
}

// 修改密码
const changePassword = async () => {
  if (!passwordForm.value.old_password) {
    ElMessage.warning('请输入当前密码')
    return
  }
  if (!passwordForm.value.new_password) {
    ElMessage.warning('请输入新密码')
    return
  }
  if (passwordForm.value.new_password.length < 6) {
    ElMessage.warning('新密码长度不能少于6位')
    return
  }
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    ElMessage.warning('两次输入的新密码不一致')
    return
  }
  if (passwordForm.value.old_password === passwordForm.value.new_password) {
    ElMessage.warning('新密码不能与当前密码相同')
    return
  }
  
  changingPassword.value = true
  try {
    await api.post('/auth/change-password', {
      old_password: passwordForm.value.old_password,
      new_password: passwordForm.value.new_password
    })
    ElMessage.success('密码修改成功')
    passwordForm.value = {
      old_password: '',
      new_password: '',
      confirm_password: ''
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '密码修改失败')
  } finally {
    changingPassword.value = false
  }
}

// 保存偏好设置
const savePreferences = () => {
  localStorage.setItem('userPreferences', JSON.stringify(preferences.value))
  ElMessage.success('偏好设置已保存')
}

// 格式化日期
const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.profile {
  max-width: 1200px;
  margin: 0 auto;
  padding: 80px 48px;
}

.page-header {
  margin-bottom: 48px;
}

.page-title {
  font-size: 48px;
  font-weight: 900;
  letter-spacing: -2px;
  margin-bottom: 12px;
  position: relative;
  display: inline-block;
  color: var(--text-primary);
}

.page-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 80px;
  height: 4px;
  background: var(--accent);
  border-radius: 2px;
}

.page-subtitle {
  font-size: 16px;
  color: var(--text-secondary);
  margin-top: 24px;
}

.profile-content {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 32px;
  align-items: start;
}

/* 侧边栏 */
.profile-sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 用户卡片 */
.user-card {
  background: var(--bg-dark);
  border-radius: 20px;
  padding: 40px 24px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.user-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--accent) 0%, var(--accent-hover) 100%);
}

.user-avatar-wrapper {
  position: relative;
  display: inline-block;
  margin-bottom: 16px;
}

.user-avatar {
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-hover) 100%);
  font-size: 36px;
  font-weight: 700;
  color: white;
  border: 4px solid rgba(255, 255, 255, 0.2);
}

.avatar-ring {
  position: absolute;
  inset: -6px;
  border: 2px solid var(--accent);
  border-radius: 50%;
  opacity: 0.5;
}

.user-name {
  font-size: 22px;
  font-weight: 800;
  color: white;
  margin-bottom: 6px;
}

.user-email {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 20px;
}

.user-stats {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  padding: 16px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-value {
  font-size: 18px;
  font-weight: 800;
  color: var(--accent);
}

.stat-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: rgba(255, 255, 255, 0.5);
}

.stat-divider {
  width: 1px;
  height: 32px;
  background: rgba(255, 255, 255, 0.1);
}

.user-bio {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.5;
}

/* 设置菜单 */
.settings-menu {
  background: white;
  border-radius: 16px;
  padding: 12px;
  border: 1px solid var(--border);
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 14px 16px;
  border: none;
  background: transparent;
  border-radius: 10px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  transition: all 0.2s;
  text-align: left;
}

.menu-item:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.menu-item.active {
  background: var(--accent-light);
  color: var(--accent);
}

.menu-item .el-icon {
  font-size: 18px;
}

/* 主内容区 */
.profile-main {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.edit-card {
  background: white;
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 32px;
  box-shadow: var(--shadow-sm);
}

.card-header {
  margin-bottom: 28px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border);
}

.card-title {
  font-size: 20px;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.card-subtitle {
  font-size: 14px;
  color: var(--text-muted);
}

/* 表单样式 */
.profile-form :deep(.el-form-item__label),
.password-form :deep(.el-form-item__label) {
  font-weight: 700;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-primary);
}

.profile-form :deep(.el-input__wrapper),
.password-form :deep(.el-input__wrapper) {
  border-radius: 10px;
  padding: 14px 16px;
}

.profile-form :deep(.el-input__wrapper:hover),
.password-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--accent);
}

.profile-form :deep(.el-input__wrapper.is-focus),
.password-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px var(--accent-light) !important;
}

.profile-form :deep(.el-textarea__inner) {
  border-radius: 10px;
  padding: 14px 16px;
  resize: none;
}

.profile-form :deep(.el-button--primary),
.password-form :deep(.el-button--primary) {
  background: var(--accent);
  border-color: var(--accent);
  font-weight: 700;
  padding: 16px 32px;
  border-radius: 10px;
}

.profile-form :deep(.el-button--primary:hover),
.password-form :deep(.el-button--primary:hover) {
  background: var(--accent-hover);
  border-color: var(--accent-hover);
}

/* 头像上传 */
.avatar-upload {
  display: flex;
  align-items: center;
  gap: 24px;
}

.preview-avatar {
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-hover) 100%);
  font-size: 28px;
  font-weight: 700;
  color: white;
  border: 3px solid var(--border);
}

.avatar-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.avatar-actions :deep(.el-button) {
  border-radius: 8px;
}

.avatar-tip {
  font-size: 12px;
  color: var(--text-muted);
  margin: 0;
}

/* 安全设置 */
.security-section {
  margin-bottom: 32px;
}

.security-section:last-child {
  margin-bottom: 0;
}

.section-title {
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-muted);
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px dashed var(--border);
}

.security-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: var(--bg-secondary);
  border-radius: 10px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-muted);
}

.info-value {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

.info-value.text-muted {
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 400;
}

/* 偏好设置 */
.preferences-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.preference-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background: var(--bg-secondary);
  border-radius: 12px;
  transition: background 0.2s;
}

.preference-item:hover {
  background: #f0f0f0;
}

.preference-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.preference-label {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

.preference-desc {
  font-size: 13px;
  color: var(--text-muted);
}

.preferences-actions {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid var(--border);
}

.preferences-actions :deep(.el-button--primary) {
  background: var(--accent);
  border-color: var(--accent);
}

.preferences-actions :deep(.el-button--primary:hover) {
  background: var(--accent-hover);
  border-color: var(--accent-hover);
}

/* 响应式 */
@media (max-width: 1024px) {
  .profile-content {
    grid-template-columns: 1fr;
  }
  
  .profile-sidebar {
    flex-direction: row;
    flex-wrap: wrap;
  }
  
  .user-card {
    flex: 1;
    min-width: 280px;
  }
  
  .settings-menu {
    flex: 1;
    min-width: 280px;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
  }
  
  .menu-item {
    flex: 1;
    min-width: 120px;
  }
}

@media (max-width: 768px) {
  .profile {
    padding: 60px 20px;
  }
  
  .page-title {
    font-size: 36px;
  }
  
  .edit-card {
    padding: 24px;
  }
  
  .profile-sidebar {
    flex-direction: column;
  }
  
  .user-card,
  .settings-menu {
    width: 100%;
  }
}
</style>
