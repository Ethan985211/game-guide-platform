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
        href="https://vmssr.com?code=fGN3KQqi"
        target="_blank"
        rel="noopener"
        class="promo-btn promo-vmssr"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 20h9M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z"/>
        </svg>
        了解更多
      </a>
    </div>
  </div>
</template>

<script setup>
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
</style>
