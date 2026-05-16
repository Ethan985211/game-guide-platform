<template>
  <div class="auth-page" @mousemove="handleMouseMove">
    <!-- 指针互动光效 -->
    <div 
      class="cursor-glow" 
      :style="cursorStyle"
    ></div>
    <!-- 浮动粒子 -->
    <div class="particles">
      <div 
        v-for="i in 12" 
        :key="i" 
        class="particle"
        :style="getParticleStyle(i)"
      ></div>
    </div>
    
    <div class="form-container">
      <div class="form-card">
        <h2>欢迎回来</h2>
        <p>登录你的账号，继续探索游戏世界</p>
        
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label>邮箱</label>
            <input 
              v-model="form.email" 
              type="email" 
              placeholder="输入邮箱地址"
              required
            >
          </div>
          
          <div class="form-group">
            <label>密码</label>
            <input 
              v-model="form.password" 
              type="password" 
              placeholder="输入密码"
              required
            >
          </div>
          
          <!-- 图形验证码 -->
          <CaptchaVerify 
            ref="captchaVerifyRef"
            v-model="captchaCode" 
          />
          
          <button type="submit" :disabled="loading || captchaCode.length !== 4">
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </form>
        
        <div class="form-footer">
          还没有账号？ <router-link to="/register">立即注册</router-link>
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

const router = useRouter()
const authStore = useAuthStore()

// 鼠标位置
const mouseX = ref(0)
const mouseY = ref(0)

// 处理鼠标移动
const handleMouseMove = (e) => {
  mouseX.value = e.clientX
  mouseY.value = e.clientY
}

// 计算光效位置
const cursorStyle = computed(() => ({
  left: mouseX.value + 'px',
  top: mouseY.value + 'px'
}))

// 生成粒子随机样式
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
  email: '',
  password: ''
})
const loading = ref(false)
const captchaCode = ref('')
const captchaVerifyRef = ref(null)

const handleLogin = async () => {
  if (!captchaCode.value) {
    ElMessage.warning('请输入验证码')
    return
  }

  loading.value = true
  try {
    await authStore.login(form.value.email, form.value.password)
    router.push('/')
  } catch (err) {
    const detail = err.response?.data?.detail
    if (detail) {
      ElMessage.error(detail)
    } else if (err.message) {
      ElMessage.error(err.message)
    } else {
      ElMessage.error('登录失败，请检查邮箱和密码')
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

/* 指针光效 */
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

/* 浮动粒子 */
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
