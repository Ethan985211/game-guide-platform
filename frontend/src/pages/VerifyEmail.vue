<template>
  <div class="verify-email-page">
    <div class="verify-card">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>正在验证邮箱...</p>
      </div>

      <!-- 验证成功 -->
      <div v-else-if="success" class="success">
        <div class="icon-box success-icon">
          <span class="icon">✓</span>
        </div>
        <h2>邮箱验证成功！</h2>
        <p>恭喜您已完成邮箱验证，现在可以享受完整的服务。</p>
        <div class="actions">
          <router-link to="/" class="btn btn-primary">返回首页</router-link>
          <router-link v-if="isLoggedIn" to="/profile" class="btn btn-secondary">完善资料</router-link>
          <router-link v-else to="/login" class="btn btn-secondary">立即登录</router-link>
        </div>
      </div>

      <!-- 验证失败 -->
      <div v-else-if="!success && !loading" class="error">
        <div class="icon-box error-icon">
          <span class="icon">!</span>
        </div>
        <h2>验证失败</h2>
        <p>{{ errorMessage }}</p>
        <div class="actions">
          <router-link to="/" class="btn btn-primary">返回首页</router-link>
          <button @click="goBack" class="btn btn-secondary">重新验证</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { authAPI } from '../api'
import { useUserStore } from '../stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(true)
const success = ref(false)
const errorMessage = ref('')

const isLoggedIn = computed(() => !!localStorage.getItem('token'))

onMounted(async () => {
  const { token, code, user_id } = route.query

  if (!token || !code || !user_id) {
    loading.value = false
    errorMessage.value = '验证链接不完整，请检查您点击的链接是否正确。'
    return
  }

  try {
    await authAPI.verifyEmail({ token, code, user_id: parseInt(user_id) })
    success.value = true
  } catch (error) {
    loading.value = false
    success.value = false
    errorMessage.value = error.response?.data?.detail || '验证失败，请稍后重试。'
  }
})

const goBack = () => {
  router.push('/login')
}
</script>

<style scoped>
.verify-email-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #ff8c00 0%, #ff6b00 100%);
  padding: 20px;
}

.verify-card {
  background: white;
  border-radius: 20px;
  padding: 50px 40px;
  max-width: 480px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  text-align: center;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 107, 0, 0.2);
  border-top-color: #ff6b00;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading p {
  color: #666;
  font-size: 16px;
}

.icon-box {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 30px;
}

.success-icon {
  background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
}

.error-icon {
  background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
}

.icon {
  font-size: 40px;
  color: white;
  font-weight: bold;
}

h2 {
  margin: 0 0 15px;
  font-size: 28px;
  color: #333;
}

p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 30px;
}

.actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 12px 30px;
  border-radius: 25px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s;
  border: none;
  cursor: pointer;
  font-size: 15px;
}

.btn-primary {
  background: linear-gradient(135deg, #ff8c00 0%, #ff6b00 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(255, 107, 0, 0.4);
}

.btn-secondary {
  background: #f5f5f5;
  color: #666;
}

.btn-secondary:hover {
  background: #e0e0e0;
}
</style>
