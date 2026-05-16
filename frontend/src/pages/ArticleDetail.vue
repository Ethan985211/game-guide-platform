<template>
  <div class="article-detail" v-if="article">
    <!-- 阅读进度条 -->
    <div class="reading-progress" :style="{ width: progressPercent + '%' }"></div>

    <!-- 头部横幅 -->
    <div class="article-hero" v-if="article.cover_image">
      <div class="article-hero-bg" :style="{ backgroundImage: `url(${article.cover_image})` }"></div>
      <div class="article-hero-gradient"></div>
      <div class="article-hero-content">
        <div class="hero-top-meta">
          <router-link v-if="article.game" :to="`/games/${article.game.id}`" class="hero-game-pill">
            {{ article.game.name }}
          </router-link>
          <span class="hero-category">{{ categoryLabel(article.category) }}</span>
          <span class="hero-date">{{ formatDate(article.created_at) }}</span>
        </div>
        <h1 class="hero-title">{{ article.title }}</h1>
      </div>
    </div>

    <!-- 主体 -->
    <div class="article-body" :class="{ 'no-hero': !article.cover_image }">
      <article class="article-main" ref="articleMain">
        <!-- 无图时的标题 -->
        <template v-if="!article.cover_image">
          <div class="article-meta-top">
            <router-link v-if="article.game" :to="`/games/${article.game.id}`" class="game-link">
              {{ article.game.name }}
            </router-link>
            <span class="meta-sep">·</span>
            <span class="category-tag">{{ categoryLabel(article.category) }}</span>
            <span class="meta-sep">·</span>
            <span class="article-date">{{ formatDate(article.created_at) }}</span>
          </div>
          <h1 class="article-title-fallback">{{ article.title }}</h1>
        </template>

        <!-- 作者卡片 -->
        <div class="author-card">
          <div class="author-main">
            <div class="author-avatar" :class="avatarColor">
              {{ article.author?.username?.[0] || 'A' }}
            </div>
            <div class="author-info">
              <span class="author-name">{{ article.author?.username || '管理员' }}</span>
              <span class="author-role">{{ article.author?.bio || '游戏攻略创作者' }}</span>
            </div>
          </div>
          <div class="article-stats">
            <div class="stat-pill">
              <span class="stat-num">{{ formatNum(article.views || 0) }}</span>
              <span class="stat-txt">阅读</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-pill">
              <span class="stat-num">{{ formatNum(article.likes || 0) }}</span>
              <span class="stat-txt">点赞</span>
            </div>
          </div>
        </div>

        <!-- 正文 -->
        <div class="article-content" v-html="formattedContent"></div>

        <!-- 标签区 -->
        <div class="article-tags" v-if="article.game">
          <router-link :to="`/games/${article.game.id}`" class="article-tag">
            {{ article.game.name }}
          </router-link>
          <span class="article-tag">{{ categoryLabel(article.category) }}</span>
          <span class="article-tag" v-if="article.game.category">{{ article.game.category }}</span>
        </div>

        <!-- 底部操作区 -->
        <div class="article-footer">
          <div class="footer-left">
            <button class="btn-like" :class="{ liked }" @click="handleLike">
              <span class="like-icon">{{ liked ? '❤️' : '🤍' }}</span>
              <span>点赞</span>
              <span class="like-count">{{ article.likes || 0 }}</span>
            </button>
            <button class="btn-share" @click="handleShare">
              <span>🔗</span> 分享
            </button>
          </div>
          <router-link to="/articles" class="btn-back">← 返回攻略列表</router-link>
        </div>
      </article>

      <!-- 侧边栏 -->
      <aside class="article-sidebar">
        <!-- 作者卡片 -->
        <div class="sidebar-card">
          <h4>关于作者</h4>
          <div class="sidebar-author">
            <div class="sidebar-avatar" :class="avatarColor">
              {{ article.author?.username?.[0] || 'A' }}
            </div>
            <div class="sidebar-author-info">
              <span class="sidebar-author-name">{{ article.author?.username || '管理员' }}</span>
              <span class="sidebar-author-bio">{{ article.author?.bio || '游戏攻略创作者' }}</span>
            </div>
          </div>
        </div>

        <!-- 相关游戏 -->
        <div class="sidebar-card" v-if="article.game">
          <h4>相关游戏</h4>
          <router-link :to="`/games/${article.game.id}`" class="sidebar-game">
            <div class="sidebar-game-img">
              <img
                :src="article.game.cover_image || article.cover_image || ''"
                :alt="article.game.name"
                @error="onImgError"
              />
            </div>
            <div class="sidebar-game-info">
              <span class="sidebar-game-name">{{ article.game.name }}</span>
              <span class="sidebar-game-cat">{{ article.game.category }}</span>
            </div>
          </router-link>
        </div>

        <!-- 文章信息 -->
        <div class="sidebar-card">
          <h4>文章信息</h4>
          <div class="sidebar-info-list">
            <div class="sidebar-info-item">
              <span class="info-label">发布</span>
              <span class="info-value">{{ formatDate(article.created_at) }}</span>
            </div>
            <div class="sidebar-info-item">
              <span class="info-label">分类</span>
              <span class="info-value">{{ categoryLabel(article.category) }}</span>
            </div>
            <div class="sidebar-info-item">
              <span class="info-label">阅读</span>
              <span class="info-value">{{ formatNum(article.views || 0) }} 次</span>
            </div>
            <div class="sidebar-info-item">
              <span class="info-label">点赞</span>
              <span class="info-value">{{ formatNum(article.likes || 0) }} 次</span>
            </div>
          </div>
        </div>
      </aside>
    </div>
  </div>

  <div v-else-if="loading" class="loading-state">
    <div class="loading-spinner"></div>
    <p>加载中...</p>
  </div>
  <div v-else class="empty-state">
    <p>文章不存在或已被删除</p>
    <router-link to="/articles">返回攻略列表</router-link>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { articleAPI } from '../api'
import { markdownToHtml } from '../utils/markdown.js'

const route = useRoute()
const article = ref(null)
const loading = ref(true)
const liked = ref(false)
const progressPercent = ref(0)
const articleMain = ref(null)

const avatarColors = ['avatar-purple', 'avatar-blue', 'avatar-green', 'avatar-orange', 'avatar-pink']
const avatarColor = computed(() => {
  const name = article.value?.author?.username || 'A'
  const idx = name.charCodeAt(0) % avatarColors.length
  return avatarColors[idx]
})

const categoryLabel = (cat) => {
  const m = { guide: '攻略', tips: '心得', news: '资讯' }
  return m[cat] || cat || '文章'
}

const formatNum = (n) => {
  if (n >= 10000) return (n / 10000).toFixed(1) + '万'
  if (n >= 1000) return (n / 1000).toFixed(1) + 'k'
  return n
}

const formattedContent = computed(() => {
  if (!article.value?.content) return ''
  return markdownToHtml(article.value.content)
})

const onImgError = (e) => {
  e.target.style.display = 'none'
}

const handleLike = async () => {
  try {
    const response = await articleAPI.likeArticle(route.params.id)
    article.value.likes = response.data.likes
    liked.value = true
    ElMessage.success('点赞成功！')
  } catch {
    ElMessage.error('点赞失败')
  }
}

const handleShare = () => {
  const url = window.location.href
  if (navigator.clipboard) {
    navigator.clipboard.writeText(url).then(() => {
      ElMessage.success('链接已复制到剪贴板')
    })
  } else {
    ElMessage.info('当前地址：' + url)
  }
}

const handleScroll = () => {
  if (!articleMain.value) return
  const rect = articleMain.value.getBoundingClientRect()
  const totalHeight = articleMain.value.scrollHeight - window.innerHeight
  if (totalHeight <= 0) {
    progressPercent.value = 100
    return
  }
  const scrolled = -rect.top
  progressPercent.value = Math.min(100, Math.max(0, (scrolled / totalHeight) * 100))
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(async () => {
  try {
    const res = await articleAPI.getArticle(route.params.id)
    article.value = res.data
  } catch (err) {
    console.error('加载失败', err)
  } finally {
    loading.value = false
  }
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
/* 阅读进度条 */
.reading-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--accent), #ff6b6b);
  z-index: 1000;
  transition: width 0.15s linear;
}

/* ============ 头部横幅 ============ */
.article-hero {
  position: relative;
  height: 420px;
  overflow: hidden;
  display: flex;
  align-items: flex-end;
}

.article-hero-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center 30%;
}

.article-hero-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(0,0,0,0.05) 0%,
    rgba(0,0,0,0.1) 30%,
    rgba(0,0,0,0.55) 60%,
    rgba(0,0,0,0.92) 100%
  );
}

.article-hero-content {
  position: relative;
  z-index: 2;
  max-width: 900px;
  margin: 0 auto;
  padding: 0 48px 56px;
  width: 100%;
}

.hero-top-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
}

.hero-game-pill {
  padding: 6px 16px;
  border-radius: 20px;
  background: rgba(255,255,255,0.18);
  backdrop-filter: blur(12px);
  color: white;
  font-size: 13px;
  font-weight: 700;
  text-decoration: none;
  letter-spacing: 0.5px;
  transition: background 0.2s;
}

.hero-game-pill:hover {
  background: rgba(255,255,255,0.32);
}

.hero-category {
  padding: 6px 14px;
  border-radius: 6px;
  background: var(--accent);
  color: white;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1px;
}

.hero-date {
  font-size: 14px;
  color: rgba(255,255,255,0.65);
}

.hero-title {
  font-size: clamp(32px, 5vw, 52px);
  font-weight: 900;
  color: white;
  line-height: 1.15;
  letter-spacing: -1.5px;
  text-shadow: 0 2px 20px rgba(0,0,0,0.4);
}

/* ============ 主体 ============ */
.article-body {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 48px 100px;
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 60px;
}

.article-body.no-hero {
  padding-top: 80px;
}

.article-main {
  min-width: 0;
}

/* 无图时的顶部 */
.article-meta-top {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.game-link {
  padding: 5px 14px;
  background: var(--accent);
  color: white;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
}

.category-tag {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 600;
}

.article-date {
  font-size: 13px;
  color: var(--text-muted);
}

.meta-sep {
  color: var(--text-muted);
  opacity: 0.3;
}

.article-title-fallback {
  font-size: clamp(28px, 5vw, 44px);
  font-weight: 900;
  letter-spacing: -1.5px;
  line-height: 1.2;
  color: var(--text-primary);
  margin-bottom: 32px;
}

/* ============ 作者卡片 ============ */
.author-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px;
  margin-bottom: 40px;
  background: var(--bg-card, white);
  border: 1px solid var(--border-color, #e8e8e8);
  border-radius: 16px;
}

.author-main {
  display: flex;
  align-items: center;
  gap: 16px;
}

.author-avatar {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 22px;
  color: white;
  flex-shrink: 0;
}

.avatar-purple { background: linear-gradient(135deg, #667eea, #764ba2); }
.avatar-blue { background: linear-gradient(135deg, #4facfe, #00f2fe); }
.avatar-green { background: linear-gradient(135deg, #43e97b, #38f9d7); }
.avatar-orange { background: linear-gradient(135deg, #fa709a, #fee140); }
.avatar-pink { background: linear-gradient(135deg, #f093fb, #f5576c); }

.author-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.author-name {
  font-weight: 700;
  font-size: 16px;
  color: var(--text-primary);
}

.author-role {
  font-size: 13px;
  color: var(--text-muted);
}

.article-stats {
  display: flex;
  align-items: center;
  gap: 0;
}

.stat-divider {
  width: 1px;
  height: 28px;
  background: var(--border-color, #e8e8e8);
  margin: 0 20px;
}

.stat-pill {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.stat-num {
  font-size: 22px;
  font-weight: 800;
  color: var(--text-primary);
}

.stat-txt {
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* ============ 正文 Markdown ============ */
.article-content {
  line-height: 1.9;
  font-size: 17px;
  color: var(--text-secondary);
  margin-bottom: 40px;
}

/* 标题层级 */
.article-content :deep(.md-h) {
  color: var(--text-primary);
  font-weight: 800;
  line-height: 1.2;
  margin: 2em 0 0.6em;
  letter-spacing: -1px;
}
.article-content :deep(.md-h1) {
  font-size: 32px;
  border-bottom: 2px solid var(--border-color, #e8e8e8);
  padding-bottom: 16px;
  margin-top: 1em;
}
.article-content :deep(.md-h2) {
  font-size: 26px;
  border-bottom: 1px solid var(--border-color, #e8e8e8);
  padding-bottom: 12px;
}
.article-content :deep(.md-h3) {
  font-size: 21px;
}
.article-content :deep(.md-h4) {
  font-size: 18px;
  color: var(--text-muted);
}

/* 段落 */
.article-content :deep(.md-p) {
  margin-bottom: 1.5em;
}

/* 粗体 / 斜体 */
.article-content :deep(strong) {
  color: var(--text-primary);
  font-weight: 700;
}
.article-content :deep(em) {
  color: var(--accent);
  font-style: italic;
}

/* 无序列表 */
.article-content :deep(.md-ul),
.article-content :deep(.md-ol) {
  margin: 1em 0 1.5em;
  padding-left: 1.5em;
}
.article-content :deep(.md-ul li),
.article-content :deep(.md-ol li) {
  margin-bottom: 0.5em;
  line-height: 1.8;
}
.article-content :deep(.md-ul) {
  list-style: disc;
}
.article-content :deep(.md-ul ul) {
  list-style: circle;
}

/* 引用块 */
.article-content :deep(.md-blockquote) {
  border-left: 4px solid var(--accent);
  background: var(--bg-secondary, #f8f8f8);
  padding: 16px 24px;
  margin: 1.5em 0;
  border-radius: 0 8px 8px 0;
  color: var(--text-secondary);
  font-size: 15px;
  line-height: 1.8;
}

/* 表格 */
.article-content :deep(.md-table-wrap) {
  overflow-x: auto;
  margin: 1.5em 0;
  border-radius: 10px;
  border: 1px solid var(--border-color, #e8e8e8);
}
.article-content :deep(.md-table) {
  width: 100%;
  border-collapse: collapse;
  font-size: 15px;
}
.article-content :deep(.md-table th) {
  background: var(--bg-secondary, #f5f5f5);
  font-weight: 700;
  color: var(--text-primary);
  text-align: left;
  padding: 12px 18px;
  border-bottom: 2px solid var(--border-color, #ddd);
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.article-content :deep(.md-table td) {
  padding: 10px 18px;
  border-bottom: 1px solid var(--border-color, #eee);
  color: var(--text-secondary);
}
.article-content :deep(.md-table tr:last-child td) {
  border-bottom: none;
}

/* 水平线 */
.article-content :deep(.md-hr) {
  border: none;
  height: 1px;
  background: var(--border-color, #e8e8e8);
  margin: 2.5em 0;
}

/* 内联代码 */
.article-content :deep(.md-inline-code) {
  background: var(--bg-secondary, #f0f0f0);
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.9em;
  font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
  color: #e65100;
}

/* 代码块 */
.article-content :deep(.md-code) {
  display: block;
  background: var(--bg-dark, #1a1a2e);
  color: #e0e0e0;
  padding: 20px 24px;
  border-radius: 10px;
  font-size: 14px;
  line-height: 1.7;
  overflow-x: auto;
  margin: 1.5em 0;
}
.article-content :deep(.md-code code) {
  font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
}

/* ============ 标签 ============ */
.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 40px;
  padding-bottom: 32px;
  border-bottom: 1px solid var(--border-color, #e8e8e8);
}

.article-tag {
  padding: 8px 18px;
  border-radius: 100px;
  font-size: 13px;
  font-weight: 600;
  border: 1px solid var(--border-color, #ddd);
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.2s;
  background: var(--bg-card, white);
}

.article-tag:hover {
  border-color: var(--accent);
  color: var(--accent);
  background: var(--accent-light, #fff5f0);
}

/* ============ 底部操作 ============ */
.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-left {
  display: flex;
  gap: 12px;
}

.btn-like {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  border: 2px solid var(--border-color, #ddd);
  border-radius: 14px;
  background: var(--bg-card, white);
  color: var(--text-primary);
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.25s;
}

.btn-like:hover {
  border-color: #ff6b6b;
  background: #fff5f5;
}

.btn-like.liked {
  border-color: #ff4757;
  background: #fff0f0;
  color: #ff4757;
}

.like-icon {
  font-size: 18px;
}

.like-count {
  opacity: 0.5;
  font-size: 13px;
}

.btn-share {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 14px 24px;
  border: 2px solid var(--border-color, #ddd);
  border-radius: 14px;
  background: var(--bg-card, white);
  color: var(--text-secondary);
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s;
}

.btn-share:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.btn-back {
  padding: 14px 28px;
  border-radius: 14px;
  color: var(--text-muted);
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s;
}

.btn-back:hover {
  color: var(--accent);
}

/* ============ 侧边栏 ============ */
.article-sidebar {
  padding-top: 24px;
}

.sidebar-card {
  position: sticky;
  top: 80px;
  padding: 24px;
  background: var(--bg-card, white);
  border-radius: 16px;
  border: 1px solid var(--border-color, #eee);
  margin-bottom: 20px;
}

.sidebar-card h4 {
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--text-muted);
  margin-bottom: 18px;
}

/* 侧边栏作者 */
.sidebar-author {
  display: flex;
  align-items: center;
  gap: 14px;
}

.sidebar-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 20px;
  color: white;
  flex-shrink: 0;
}

.sidebar-author-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.sidebar-author-name {
  font-weight: 700;
  font-size: 15px;
  color: var(--text-primary);
}

.sidebar-author-bio {
  font-size: 12px;
  color: var(--text-muted);
}

/* 相关游戏 */
.sidebar-game {
  display: flex;
  gap: 14px;
  align-items: center;
  text-decoration: none;
  padding: 12px;
  border-radius: 12px;
  transition: background 0.2s;
}

.sidebar-game:hover {
  background: var(--bg-secondary, #f5f5f5);
}

.sidebar-game-img {
  width: 56px;
  height: 56px;
  border-radius: 10px;
  overflow: hidden;
  background: var(--bg-dark);
}

.sidebar-game-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.sidebar-game-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.sidebar-game-name {
  font-weight: 700;
  font-size: 15px;
  color: var(--text-primary);
}

.sidebar-game-cat {
  font-size: 12px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* 文章信息列表 */
.sidebar-info-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.sidebar-info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-label {
  font-size: 13px;
  color: var(--text-muted);
}

.info-value {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

/* ============ 状态 ============ */
.loading-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 16px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-color);
  border-top: 3px solid var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.empty-state a {
  color: var(--accent);
  font-weight: 600;
}

@media (max-width: 900px) {
  .article-body {
    grid-template-columns: 1fr;
    padding: 0 20px 60px;
  }
  .article-body.no-hero {
    padding-top: 40px;
  }
  .article-hero {
    height: 240px;
  }
  .article-hero-content {
    padding: 0 20px 40px;
  }
  .hero-title {
    font-size: clamp(24px, 6vw, 36px);
  }
  .article-sidebar {
    display: none;
  }
  .author-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  .article-footer {
    flex-direction: column;
    gap: 16px;
  }
  .footer-left {
    width: 100%;
  }
  .btn-like, .btn-share {
    flex: 1;
    justify-content: center;
  }
}
</style>
