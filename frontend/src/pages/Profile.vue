<template>
  <div class="profile page-container">
    <h1 class="page-title">个人中心</h1>

    <el-row :gutter="24">
      <!-- 用户信息 -->
      <el-col :span="8">
        <el-card>
          <div class="user-info">
            <el-avatar :size="80">{{ authStore.user?.username?.[0] }}</el-avatar>
            <h2>{{ authStore.user?.username }}</h2>
            <p>{{ authStore.user?.email }}</p>
            <p class="bio">{{ authStore.user?.bio || '暂无简介' }}</p>
          </div>
        </el-card>
      </el-col>

      <!-- 编辑资料 -->
      <el-col :span="16">
        <el-card>
          <template #header>
            <span>编辑资料</span>
          </template>
          <el-form :model="form" label-width="80px">
            <el-form-item label="用户名">
              <el-input v-model="form.username" />
            </el-form-item>
            <el-form-item label="简介">
              <el-input v-model="form.bio" type="textarea" :rows="3" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveProfile">保存</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../stores/auth'
import api from '../api'

const authStore = useAuthStore()
const form = ref({
  username: '',
  bio: ''
})

onMounted(() => {
  form.value.username = authStore.user?.username || ''
  form.value.bio = authStore.user?.bio || ''
})

const saveProfile = async () => {
  try {
    await api.put('/auth/me', {
      username: form.value.username,
      bio: form.value.bio
    })
    await authStore.fetchUser()
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
  }
}
</script>

<style scoped>
.profile {
  padding-top: 20px;
}

.user-info {
  text-align: center;
}

.user-info h2 {
  margin-top: 16px;
  margin-bottom: 8px;
}

.user-info p {
  color: #606266;
  margin-bottom: 8px;
}

.bio {
  font-size: 14px;
  color: #909399 !important;
}
</style>
