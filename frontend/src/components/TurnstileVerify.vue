<template>
  <div class="turnstile-container">
    <!-- 开发模式提示 -->
    <div v-if="!envSitekey" class="dev-hint">
      <span>⚠️ 人机验证（演示模式）</span>
      <small>请配置 VITE_TURNSTILE_SITEKEY 使用真实验证</small>
    </div>
    
    <div 
      ref="turnstileRef" 
      class="cf-turnstile" 
      :data-sitekey="currentSitekey" 
      :data-theme="theme"
      data-callback="onTurnstileSuccess"
      data-error-callback="onTurnstileError"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

// 获取 sitekey，优先使用环境变量
const envSitekey = import.meta.env.VITE_TURNSTILE_SITEKEY || ''
// Cloudflare Turnstile 测试 sitekey（仅用于开发/演示）
const TEST_SITEKEY = '0x4AAAAAAAxxxxxxxxxxxxxxx'

const props = defineProps({
  sitekey: {
    type: String,
    default: ''
  },
  theme: {
    type: String,
    default: 'light',
    validator: (v) => ['light', 'dark', 'auto'].includes(v)
  },
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'verify', 'expire', 'error'])

// 计算最终使用的 sitekey
const currentSitekey = computed(() => {
  if (props.sitekey) return props.sitekey
  if (envSitekey) return envSitekey
  return TEST_SITEKEY
})

const turnstileRef = ref(null)
let widgetId = null

// Turnstile 全局回调函数
window.onTurnstileSuccess = (token) => {
  emit('update:modelValue', token)
  emit('verify', token)
}

window.onTurnstileError = () => {
  emit('error')
}

window.onTurnstileExpire = () => {
  emit('update:modelValue', '')
  emit('expire')
}

// 渲染 Turnstile widget
const renderWidget = () => {
  if (window.turnstile && turnstileRef.value) {
    if (widgetId) {
      try {
        window.turnstile.remove(widgetId)
      } catch (e) {}
    }
    widgetId = window.turnstile.render(turnstileRef.value, {
      sitekey: currentSitekey.value,
      theme: props.theme,
      callback: window.onTurnstileSuccess,
      'error-callback': window.onTurnstileError,
      'expired-callback': window.onTurnstileExpire
    })
  }
}

// 重置 widget
const reset = () => {
  if (window.turnstile && widgetId) {
    window.turnstile.reset(widgetId)
    emit('update:modelValue', '')
  }
}

defineExpose({ reset })

onMounted(() => {
  const checkTurnstile = setInterval(() => {
    if (window.turnstile) {
      clearInterval(checkTurnstile)
      renderWidget()
    }
  }, 100)
  setTimeout(() => clearInterval(checkTurnstile), 5000)
})

onUnmounted(() => {
  if (window.turnstile && widgetId) {
    try {
      window.turnstile.remove(widgetId)
    } catch (e) {}
  }
})

watch(() => props.theme, () => {
  reset()
  renderWidget()
})
</script>

<style scoped>
.turnstile-container {
  margin: 16px 0;
}

.dev-hint {
  background: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: 6px;
  padding: 8px 12px;
  margin-bottom: 12px;
  font-size: 13px;
  color: #856404;
}

.dev-hint small {
  display: block;
  margin-top: 2px;
  opacity: 0.8;
  font-size: 11px;
}

.cf-turnstile {
  display: flex;
  justify-content: center;
}
</style>
