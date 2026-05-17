<template>
  <div class="auth-page" @mousemove="handleMouseMove">
    <div class="cursor-glow" :style="cursorStyle"></div>
    <div class="particles">
      <div v-for="i in 12" :key="i" class="particle" :style="getParticleStyle(i)"></div>
    </div>
    
    <div class="form-container">
      <div class="form-card">
        <h2>创建账号</h2>
        <p>加入我们，开始你的游戏之旅</p>

        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label>用户名</label>
            <input
              v-model="form.username"
              type="text"
              placeholder="选择用户名"
              required
            >
          </div>

          <div class="form-group">
            <label>邮箱</label>
            <input
              v-model="form.email"
              type="email"
              placeholder="输入邮箱地址"
              required
            >
          </div>

          <!-- 图形验证码 -->
          <div class="form-group">
            <CaptchaVerify 
              ref="captchaVerifyRef"
              v-model="captchaCode" 
            />
            <button 
              type="button" 
              class="send-code-btn"
              :disabled="!canSendCode || sendingCode"
              @click="handleSendCode"
            >
              {{ sendingCode ? `${countdown}秒` : '发送验证码' }}
            </button>
          </div>

          <!-- 邮箱验证码 -->
          <div class="form-group" v-if="showEmailCode">
            <label>邮箱验证码</label>
            <input
              v-model="emailCode"
              type="text"
              placeholder="输入邮箱收到的验证码"
              maxlength="6"
              required
            >
          </div>

          <div class="form-group">
            <label>出生日期（年龄验证）</label>
            <input
              v-model="form.birth_date"
              type="date"
              required
            >
          </div>

          <div class="form-group">
            <label>密码</label>
            <input
              v-model="form.password"
              type="password"
              placeholder="设置密码（至少6位）"
              required
            >
          </div>

          <button type="submit" :disabled="loading || !canRegister">
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </form>

        <div class="form-footer">
          已有账号？ <router-link to="/login">立即登录</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../stores/auth'
import CaptchaVerify from '../components/CaptchaVerify.vue'
import api from '../api'

const router = useRouter()
const authStore = useAuthStore()

const mouseX = ref(0)
const mouseY = ref(0)

const handleMouseMove = (e) => {
  mouseX.value = e.clientX
  mouseY.value = e.clientY
}

const cursorStyle = computed(() => ({
  left: mouseX.value + 'px',
  top: mouseY.value + 'px'
}))

const getParticleStyle = (i) => {
  const size = 6 + (i % 4) * 4
  const delay = (i * 0.5) % 3
  const duration = 15 + (i % 5) * 3
  const left = (i * 8 + (i % 3) * 15) % 100
  const top = (i * 7 + (i % 4) * 20) % 100
  return {
    width: size + 'px',
    height: size + 'px',
    left: left + '%',
    top: top + '%',
    animationDelay: -delay + 's',
    animationDuration: duration + 's'
  }
}

const form = ref({
  username: '',
  email: '',
  password: '',
  birth_date: '2000-01-01'
})

const loading = ref(false)
const captchaCode = ref('')
const captchaVerifyRef = ref(null)
const emailCode = ref('')
const showEmailCode = ref(false)
const sendingCode = ref(false)
const countdown = ref(0)
const codeSent = ref(false)

// 图形验证码通过后才能发送
const canSendCode = computed(() => {
  return form.value.email && captchaCode.value.length === 4
})

// 所有验证通过才能注册
const canRegister = computed(() => {
  return form.value.username && 
         form.value.email && 
         form.value.password.length >= 6 &&
         emailCode.value.length === 6
})

// 发送邮箱验证码
const handleSendCode = async () => {
  if (countdown.value > 0) return
  
  sendingCode.value = true
  try {
    await api.post('/auth/send-register-code', {
      email: form.value.email
    })
    ElMessage.success('验证码已发送到邮箱')
    showEmailCode.value = true
    codeSent.value = true
    
    // 开始倒计时
    countdown.value = 60
    const timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(timer)
      }
    }, 1000)
  } catch (err) {
    const detail = err.response?.data?.detail
    ElMessage.error(detail || '发送失败')
  } finally {
    sendingCode.value = false
  }
}

const handleRegister = async () => {
  if (form.value.password.length < 6) {
    ElMessage.warning('密码至少需要6位')
    return
  }

  loading.value = true
  try {
    await api.post('/auth/register', {
      username: form.value.username,
      email: form.value.email,
      password: form.value.password,
      birth_date: form.value.birth_date,
      code: emailCode.value
    })
    ElMessage.success('注册成功！')
    // 自动登录
    await authStore.login(form.value.email, form.value.password)
    router.push('/')
  } catch (err) {
    const detail = err.response?.data?.detail
    if (detail) {
      ElMessage.error(detail)
    } else if (err.message) {
      ElMessage.error(err.message)
    } else {
      ElMessage.error('注册失败，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  position: relative;
  min-height: calc(100vh - 64px);
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  overflow: hidden;
}

.cursor-glow {
  position: fixed;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 140, 0, 0.08) 0%, rgba(255, 107, 0, 0.03) 40%, transparent 70%);
  pointer-events: none;
  transform: translate(-50%, -50%);
  z-index: 0;
  transition: background 0.3s ease;
}

.particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

.particle {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(255, 140, 0, 0.4), rgba(255, 107, 0, 0.2));
  animation: float linear infinite;
  opacity: 0.6;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) translateX(0) scale(1);
    opacity: 0.6;
  }
  25% {
    transform: translateY(-30px) translateX(10px) scale(1.1);
    opacity: 0.8;
  }
  50% {
    transform: translateY(-20px) translateX(-10px) scale(0.9);
    opacity: 0.5;
  }
  75% {
    transform: translateY(-40px) translateX(5px) scale(1.05);
    opacity: 0.7;
  }
}

.form-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 420px;
}

.form-card {
  background: #ffffff;
  padding: 48px 40px;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  position: relative;
  overflow: hidden;
}

.form-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #ff8c00, #ff6b00, #ff8c00);
}

.form-card h2 {
  text-align: center;
  color: #1a1a1a;
  margin-bottom: 8px;
  font-size: 28px;
  font-weight: 700;
  letter-spacing: 2px;
}

.form-card > p {
  text-align: center;
  color: #666;
  margin-bottom: 36px;
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
  letter-spacing: 1px;
}

.form-group input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 15px;
  transition: all 0.3s ease;
  background: #fafafa;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #ff8c00;
  box-shadow: 0 0 0 4px rgba(255, 140, 0, 0.15);
  background: #fff;
}

.form-group input::placeholder {
  color: #aaa;
}

/* 发送验证码按钮 */
.send-code-btn {
  width: 100%;
  margin-top: 12px;
  padding: 12px 16px;
  background: #fff;
  color: #ff6b00;
  border: 2px solid #ff8c00;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.send-code-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #ff8c00 0%, #ff6b00 100%);
  color: #fff;
  border-color: transparent;
}

.send-code-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  color: #999;
  border-color: #ddd;
}

button[type="submit"] {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #ff8c00 0%, #ff6b00 100%);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 12px;
  letter-spacing: 2px;
  text-transform: uppercase;
  box-shadow: 0 4px 15px rgba(255, 107, 0, 0.3);
}

button[type="submit"]:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 107, 0, 0.4);
}

button[type="submit"]:active:not(:disabled) {
  transform: translateY(-1px);
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.form-footer {
  text-align: center;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #eee;
  color: #666;
  font-size: 14px;
}

.form-footer a {
  color: #ff8c00;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s;
}

.form-footer a:hover {
  color: #ff6b00;
  text-decoration: underline;
}

@media (max-width: 480px) {
  .form-card {
    padding: 32px 24px;
  }
  
  .form-card h2 {
    font-size: 24px;
  }
}
</style>
