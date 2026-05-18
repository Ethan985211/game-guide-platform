<template>
  <div class="promo-card">
    <h4 class="promo-title">支持本站</h4>
    <p class="promo-desc">本站内容全部免费，如果对你有帮助，可以通过以下方式支持我们</p>
    <div class="promo-links">
      <a
        href="https://www.aliyun.com/minisite/goods?userCode=xqdanc4i"
        target="_blank"
        rel="noopener"
        class="promo-btn promo-aliyun"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"/>
          <path d="M2 12h20M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10M12 2a15.3 15.3 0 00-4 10 15.3 15.3 0 004 10"/>
        </svg>
        购买即支持本站
      </a>
      <a
        href="https://apikey.fun/register?aff=DFWDYXJJCFSW"
        target="_blank"
        rel="noopener"
        class="promo-btn promo-vmssr"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 2l7 7-7 7-7-7 7-7z"/>
          <path d="M12 22V9"/>
        </svg>
        代理服务
      </a>
    </div>
    <button class="promo-donate" @click="showDonate = true">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/>
      </svg>
      打赏支持
    </button>

    <!-- 打赏弹窗 -->
    <Teleport to="body">
      <div v-if="showDonate" class="donate-overlay" @click.self="showDonate = false">
        <div class="donate-modal">
          <button class="donate-close" @click="showDonate = false">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
          <h3>感谢支持</h3>
          <p>扫码打赏，支持我们持续更新优质攻略内容</p>
          <div class="donate-codes">
            <div class="donate-item">
              <img src="/支付宝收款码.jpeg" alt="支付宝收款码" />
              <span>支付宝</span>
            </div>
            <div class="donate-item">
              <img src="/微信收款码.jpeg" alt="微信收款码" />
              <span>微信支付</span>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showDonate = ref(false)
</script>

<style scoped>
.promo-card {
  padding: 24px;
  border-radius: 14px;
  background: var(--bg-card, #fff);
  border: 1px solid var(--border-color, #e8e8e8);
}

.promo-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.promo-desc {
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.6;
  margin-bottom: 16px;
}

.promo-links {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.promo-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.promo-aliyun {
  background: linear-gradient(135deg, #ff6b00, #ff4444);
  color: white;
}
.promo-aliyun:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
}

.promo-vmssr {
  background: var(--bg-secondary, #f5f5f5);
  color: var(--text-secondary);
  border: 1px solid var(--border-color, #e8e8e8);
}
.promo-vmssr:hover {
  background: var(--bg-primary, #fff);
  border-color: var(--accent, #ff6b00);
  color: var(--accent, #ff6b00);
}

.promo-donate {
  width: 100%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  border: 1px dashed var(--border-color, #e8e8e8);
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s;
}
.promo-donate:hover {
  border-color: var(--accent, #ff6b00);
  color: var(--accent, #ff6b00);
  background: rgba(255, 107, 0, 0.04);
}

/* 打赏弹窗 */
.donate-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.donate-modal {
  background: var(--bg-card, #fff);
  border-radius: 20px;
  padding: 40px;
  max-width: 440px;
  width: 100%;
  position: relative;
  text-align: center;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.2);
}

.donate-close {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: var(--bg-secondary, #f5f5f5);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  transition: all 0.2s;
}
.donate-close:hover {
  background: var(--border-color, #e8e8e8);
  color: var(--text-primary);
}

.donate-modal h3 {
  font-size: 22px;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 8px;
  letter-spacing: -0.5px;
}

.donate-modal > p {
  font-size: 14px;
  color: var(--text-muted);
  margin-bottom: 32px;
  line-height: 1.6;
}

.donate-codes {
  display: flex;
  gap: 24px;
  justify-content: center;
}

.donate-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.donate-item img {
  width: 160px;
  height: 160px;
  border-radius: 12px;
  border: 1px solid var(--border-color, #eee);
  object-fit: contain;
}

.donate-item span {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
}
</style>
