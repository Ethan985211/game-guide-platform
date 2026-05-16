<template>
  <div class="not-found">
    <div class="card">
      <h1 class="code">404</h1>
      <p class="desc">页面未找到</p>
      <p class="hint">你访问的页面不存在或已被移除</p>
      <router-link to="/" class="btn-home">返回首页</router-link>
    </div>
  </div>
</template>

<style scoped>
.not-found {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  padding: 20px;
}
.card {
  text-align: center;
  max-width: 480px;
  padding: 48px 40px;
  background: var(--bg-card);
  border-radius: 16px;
  border: 1px solid var(--border-color);
}
.code {
  font-size: 96px;
  font-weight: 900;
  color: var(--accent);
  margin: 0;
  line-height: 1;
  letter-spacing: -4px;
}
.desc {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 16px 0 8px;
}
.hint {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0 0 32px;
}
.btn-home {
  display: inline-block;
  padding: 12px 32px;
  background: var(--accent);
  color: white;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 15px;
  transition: transform 0.2s, box-shadow 0.2s;
}
.btn-home:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 107, 0, 0.35);
}
</style>
