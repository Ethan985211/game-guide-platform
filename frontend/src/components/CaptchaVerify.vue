<template>
  <div class="captcha-container">
    <div class="captcha-box" @click="refreshCode">
      <canvas ref="canvasRef" width="120" height="40"></canvas>
    </div>
    <input
      v-model="userInput"
      type="text"
      placeholder="输入验证码"
      maxlength="4"
      class="captcha-input"
      @input="handleInput"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const emit = defineEmits(['update:modelValue', 'verify'])

const canvasRef = ref(null)
const captchaCode = ref('')
const userInput = ref('')

// 生成随机验证码（仅使用小写字母和数字，便于用户输入）
const generateCode = () => {
  const chars = 'abcdefghjkmnpqrstuvwxyz23456789'
  let code = ''
  for (let i = 0; i < 4; i++) {
    code += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  captchaCode.value = code
  drawCanvas()
}

// 绘制验证码到 canvas
const drawCanvas = () => {
  const canvas = canvasRef.value
  if (!canvas) return
  
  const ctx = canvas.getContext('2d')
  const width = canvas.width
  const height = canvas.height
  
  // 清空画布
  ctx.fillStyle = '#f0f0f0'
  ctx.fillRect(0, 0, width, height)
  
  // 绘制背景线
  ctx.strokeStyle = '#ddd'
  for (let i = 0; i < 5; i++) {
    ctx.beginPath()
    ctx.moveTo(Math.random() * width, Math.random() * height)
    ctx.lineTo(Math.random() * width, Math.random() * height)
    ctx.stroke()
  }
  
  // 绘制验证码文字
  ctx.font = 'bold 24px Arial'
  ctx.fillStyle = '#333'
  const textWidth = ctx.measureText(captchaCode.value).width
  const startX = (width - textWidth) / 2
  const startY = height / 2 + 8
  
  for (let i = 0; i < captchaCode.value.length; i++) {
    const char = captchaCode.value[i]
    const offsetX = (i - 1.5) * 18
    const rotation = (Math.random() - 0.5) * 0.4
    const color = `hsl(${Math.random() * 60 + 200}, 60%, 40%)`
    
    ctx.save()
    ctx.translate(startX + offsetX + 20, startY)
    ctx.rotate(rotation)
    ctx.fillStyle = color
    ctx.fillText(char, 0, 0)
    ctx.restore()
  }
  
  // 绘制干扰点
  for (let i = 0; i < 30; i++) {
    ctx.fillStyle = `rgba(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255}, 0.5)`
    ctx.beginPath()
    ctx.arc(Math.random() * width, Math.random() * height, 1, 0, Math.PI * 2)
    ctx.fill()
  }
}

// 刷新验证码
const refreshCode = () => {
  generateCode()
  userInput.value = ''
  emit('update:modelValue', '')
}

// 处理输入
const handleInput = () => {
  const value = userInput.value.toLowerCase()
  emit('update:modelValue', value)
  
  // 实时验证（可选）
  if (value.length === 4) {
    emit('verify', value)
  }
}

// 暴露刷新方法
defineExpose({ refreshCode, getCode: () => captchaCode.value })

onMounted(() => {
  generateCode()
})

watch(() => canvasRef.value, () => {
  if (canvasRef.value) {
    generateCode()
  }
})
</script>

<style scoped>
.captcha-container {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.captcha-box {
  position: relative;
  cursor: pointer;
  border-radius: 10px;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-right: 12px;
}

.captcha-box:hover {
  transform: scale(1.03);
  box-shadow: 0 4px 12px rgba(255, 140, 0, 0.2);
}

.captcha-box canvas {
  display: block;
}

.refresh-hint {
  position: absolute;
  bottom: 3px;
  right: 5px;
  font-size: 9px;
  color: #666;
  background: rgba(255,255,255,0.9);
  padding: 2px 4px;
  border-radius: 3px;
}

.captcha-input {
  min-width: 0;
  max-width: 140px;
  width: 100%;
  padding: 12px 14px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 15px;
  font-family: monospace;
  letter-spacing: 3px;
  text-transform: uppercase;
  transition: all 0.3s ease;
  background: #fafafa;
  box-sizing: border-box;
}

.captcha-input:focus {
  outline: none;
  border-color: #ff8c00;
  box-shadow: 0 0 0 4px rgba(255, 140, 0, 0.15);
  background: #fff;
}
</style>
