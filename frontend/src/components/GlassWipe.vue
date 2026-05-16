<template>
  <div class="glass-wipe-container">
    <!-- 背景层 - 静态模糊的Logo -->
    <div class="bg-pattern" :style="maskStyle">
      <div class="logo-grid">
        <span class="logo-text" v-for="i in 60" :key="i">Game<span>Hub</span></span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  mouseX: {
    type: Number,
    default: 250
  },
  mouseY: {
    type: Number,
    default: 250
  }
})

const maskStyle = computed(() => ({
  '--mouse-x': `${props.mouseX}px`,
  '--mouse-y': `${props.mouseY}px`,
}))
</script>

<style scoped>
.glass-wipe-container {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

/* 背景层 - 静态网格布局 */
.bg-pattern {
  position: absolute;
  inset: 0;
  display: flex;
  flex-wrap: wrap;
  align-content: flex-start;
  padding: 20px;
  -webkit-mask-image: radial-gradient(
    circle 120px at var(--mouse-x) var(--mouse-y),
    white 0px,
    white 80px,
    transparent 120px
  );
  mask-image: radial-gradient(
    circle 120px at var(--mouse-x) var(--mouse-y),
    white 0px,
    white 80px,
    transparent 120px
  );
  transition: --mouse-x 0.3s ease-out, --mouse-y 0.3s ease-out;
}

.logo-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 30px 60px;
  width: 100%;
}

.logo-text {
  display: inline;
  font-size: clamp(28px, 4vw, 48px);
  font-weight: 900;
  letter-spacing: 2px;
  color: var(--text-primary);
  text-transform: uppercase;
  opacity: 0.4;
  white-space: nowrap;
  transition: opacity 0.3s;
}

.logo-text span {
  display: inline;
  color: var(--accent);
  font-weight: 900;
  font-size: 1.3em;
}
</style>
