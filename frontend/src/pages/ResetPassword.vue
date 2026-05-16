<template>
  <div class="reset-password-page">
    <div class="reset-card">
      <!-- 初始状态 - 申请重置 -->
      <div v-if="step === 'request' && !resetSuccess" class="step request">
        <div class="icon-box">
          <span class="icon">重置</span>
        </div>
        <h2>忘记密码？</h2>
        <p>输入您的注册邮箱，我们会发送重置链接到您的邮箱。</p>

        <form @submit.prevent="handleRequestReset" class="form">
          <div class="input-group">
            <input
              v-model="email"
              type="email"
              placeholder="请输入邮箱地址"
              :disabled="loading"
              required
            />
          </div>

          <p v-if="message" class="message" :class="messageType">{{ message }}</p>

          <button type="submit" class="btn btn-primary" :disabled="loading">
            <span v-if="loading">发送中...</span>
            <span v-else>发送重置链接</span>
          </button>
        </form>

        <p class="links">
          想起密码了？<router-link to="/login">立即登录</router-link>
        </p>
      </div>

      <!-- 重置表单 -->
      <div v-else-if="step === 'reset'" class="step reset">
        <div class="icon-box">
          <span class="icon">密码</span>
        </div>
        <h2>设置新密码</h2>
        <p>请输入您的新密码。</p>

        <form @submit.prevent="handleResetPassword" class="form">
          <div class="input-group">
            <input
              v-model="newPassword"
              type="password"
              placeholder="新密码（至少8位）"
              :disabled="loading"
              required
              minlength="8"
            />
          </div>

          <div class="input-group">
            <input
              v-model="confirmPassword"
              type="password"
              placeholder="确认新密码"
              :disabled="loading"
              required
            />
          </div>

          <p v-if="passwordError" class="message error">{{ passwordError }}</p>
          <p v-if="message" class="message" :class="messageType">{{ message }}</p>

          <button type="submit" class="btn btn-primary" :disabled="loading || !!passwordError">
            <span v-if="loading">重置中...</span>
            <span v-else>确认重置</span>
          </button>
        </form>
      </div>

      <!-- 重置成功 -->
      <div v-else-if="resetSuccess" class="step success">
        <div class="icon-box success-icon">
          <span class="icon">✓</span>
        </div>
        <h2>密码重置成功！</h2>
        <p>您的密码已成功重置，请使用新密码登录。</p>

        <router-link to="/login" class="btn btn-primary">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { authAPI } from '../api'

const route = useRoute()
const router = useRouter()

const step = ref('request')
const loading = ref(false)
const message = ref('')
const messageType = ref('')
const resetSuccess = ref(false)

const email = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const token = ref('')
const userId = ref(null)

const passwordError = computed(() => {
  if (newPassword.value && confirmPassword.value) {
    if (newPassword.value !== confirmPassword.value) {
      return '两次输入的密码不一致'
    }
    if (newPassword.value.length < 8) {
      return '密码长度至少8位'
    }
  }
  return ''
})

onMounted(() => {
  const { token: queryToken, user_id } = route.query
  if (queryToken && user_id) {
    token.value = queryToken
    userId.value = parseInt(user_id)
    step.value = 'reset'
  }
})

const handleRequestReset = async () => {
  loading.value = true
  message.value = ''

  try {
    await authAPI.forgotPassword(email.value)
    message.value = '重置链接已发送到您的邮箱，请查收。'
    messageType.value = 'success'
    email.value = ''
  } catch (error) {
    message.value = error.response?.data?.detail || '发送失败，请稍后重试。'
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}

const handleResetPassword = async () => {
  if (passwordError.value) return

  loading.value = true
  message.value = ''

  try {
    await authAPI.resetPassword({
      token: token.value,
      user_id: userId.value,
      new_password: newPassword.value
    })
    resetSuccess.value = true
    step.value = 'success'
  } catch (error) {
    message.value = error.response?.data?.detail || '重置失败，请稍后重试。'
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.reset-password-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  padding: 20px;
}

.reset-card {
  background: white;
  border-radius: 20px;
  padding: 50px 40px;
  max-width: 420px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  text-align: center;
}

.icon-box {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 25px;
}

.success-icon {
  background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
}

.icon {
  font-size: 18px;
  color: white;
  font-weight: bold;
}

h2 {
  margin: 0 0 12px;
  font-size: 26px;
  color: #333;
}

p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 25px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.input-group input {
  width: 100%;
  padding: 14px 18px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 15px;
  transition: all 0.3s;
  box-sizing: border-box;
}

.input-group input:focus {
  border-color: #f5576c;
  outline: none;
}

.input-group input:disabled {
  background: #f5f5f5;
}

.message {
  padding: 10px;
  border-radius: 8px;
  font-size: 14px;
  margin: 0;
}

.message.success {
  background: #d4edda;
  color: #155724;
}

.message.error {
  background: #f8d7da;
  color: #721c24;
}

.btn {
  width: 100%;
  padding: 14px;
  border-radius: 25px;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.3s;
  border: none;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  box-sizing: border-box;
}

.btn-primary {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(245, 87, 108, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.links {
  margin-top: 20px;
  font-size: 14px;
}

.links a {
  color: #f5576c;
  text-decoration: none;
  font-weight: 600;
}

.links a:hover {
  text-decoration: underline;
}

.step.success .btn {
  width: auto;
  padding: 14px 40px;
}
</style>
