<template>
  <div class="admin-login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h1>管理员登录</h1>
          <p>GameHub 后台管理系统</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label>用户名</label>
            <input
              v-model="form.username"
              type="text"
              placeholder="请输入管理员用户名"
              required
            >
          </div>

          <div class="form-group">
            <label>密码</label>
            <input
              v-model="form.password"
              type="password"
              placeholder="请输入密码"
              required
            >
          </div>

          <button type="submit" :disabled="loading">
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </form>

        <div class="back-link">
          <router-link to="/">
            <el-icon><ArrowLeft /></el-icon>
            返回首页
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAdminStore } from '../../stores/admin'
import { ArrowLeft } from '@element-plus/icons-vue'

const router = useRouter()
const adminStore = useAdminStore()

const form = ref({
  username: '',
  password: ''
})

const loading = ref(false)

const handleLogin = async () => {
  loading.value = true
  try {
    await adminStore.login(form.value.username, form.value.password)
    ElMessage.success('登录成功')
    router.push('/admin')
  } catch (err) {
    const detail = err.response?.data?.detail || '登录失败'
    ElMessage.error(detail)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.admin-login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 420px;
}

.login-card {
  background: white;
  border-radius: 16px;
  padding: 48px 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-header h1 {
  font-size: 28px;
  color: #1a1a1a;
  margin-bottom: 8px;
}

.login-header p {
  color: #666;
  font-size: 14px;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 10px;
  color: #333;
  font-weight: 600;
  font-size: 14px;
}

.form-group input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 15px;
  transition: all 0.3s;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #ff8c00;
  box-shadow: 0 0 0 4px rgba(255, 140, 0, 0.15);
}

button[type="submit"] {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #ff8c00 0%, #ff6b00 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
}

button[type="submit"]:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 107, 0, 0.4);
}

button[type="submit"]:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.back-link {
  text-align: center;
  margin-top: 24px;
}

.back-link a {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #666;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s;
}

.back-link a:hover {
  color: #ff8c00;
}
</style>
