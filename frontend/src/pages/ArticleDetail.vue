<template>
  <div class="article-detail" v-if="article">
    <!-- 文章头部横幅 -->
    <div class="article-hero" v-if="article.cover_image">
      <div class="article-hero-bg" :style="{ backgroundImage: `url(${article.cover_image})` }"></div>
      <div class="article-hero-gradient"></div>
    </div>

    <!-- 文章内容 -->
    <div class="article-body">
      <article class="article-main">
        <!-- 元信息 -->
        <div class="article-meta-top">
          <router-link
            v-if="article.game"
            :to="`/games/${article.game.id}`"
            class="article-game-link"
          >
            {{ article.game.name }}
          </router-link>
          <span class="meta-sep">·</span>
          <span class="article-category-tag">{{ categoryLabel(article.category) }}</span>
          <span class="meta-sep">·</span>
          <span class="article-date">{{ formatDate(article.created_at) }}</span>
        </div>

        <!-- 标题 -->
        <h1 class="article-title">{{ article.title }}</h1>

        <!-- 作者区 -->
        <div class="article-author">
          <div class="author-avatar">
            {{ article.author?.username?.[0] || 'A' }}
          </div>
          <div class="author-info">
            <span class="author-name">{{ article.author?.username || '管理员' }}</span>
            <span class="author-bio">{{ article.author?.bio || '游戏攻略创作者' }}</span>
          </div>
          <div class="article-stats">
            <div class="stat-pill">
              <span class="stat-num">{{ article.views || 0 }}</span>
              <span class="stat-txt">阅读</span>
            </div>
            <div class="stat-pill">
              <span class="stat-num">{{ article.likes || 0 }}</span>
              <span class="stat-txt">点赞</span>
            </div>
          </div>
        </div>

        <!-- 正文 -->
        <div class="article-content" v-html="formattedContent"></div>

        <!-- 底部操作 -->
        <div class="article-footer">
          <button class="btn-like" @click="handleLike">
            <span class="like-icon">{{ liked ? '♥' : '♡' }}</span>
            点赞 {{ article.likes }}
          </button>
          <router-link to="/articles" class="btn-back">返回攻略列表</router-link>
        </div>
      </article>

      <!-- 侧边栏 -->
      <aside class="article-sidebar" v-if="article.game">
        <div class="sidebar-card">
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
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { articleAPI } from '../api'

const route = useRoute()
const article = ref(null)
const loading = ref(true)
const liked = ref(false)

const categoryLabel = (cat) => {
  const m = { guide: '攻略', tips: '心得', news: '资讯' }
  return m[cat] || cat || '文章'
}

const formattedContent = computed(() => {
  if (!article.value?.content) return ''
  // Simple HTML-safe rendering with basic formatting
  return article.value.content
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>')
    .replace(/^/, '<p>')
    .replace(/$/, '</p>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
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
})
</script>

<style scoped>
/* 头图横幅 */
.article-hero {
  position: relative;
  height: 320px;
  overflow: hidden;
}

.article-hero-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  filter: blur(0px);
}

.article-hero-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0.1), rgba(0,0,0,0.7));
}

/* 文章主体 */
.article-body {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 48px 80px;
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 48px;
}

.article-main {
  min-width: 0;
}

/* 顶部元信息 */
.article-meta-top {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: -40px;
  margin-bottom: 24px;
  position: relative;
  z-index: 2;
}

.article-game-link {
  padding: 6px 14px;
  background: var(--accent);
  color: white;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.2s;
}

.article-game-link:hover {
  background: var(--accent-hover);
}

.article-category-tag {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 600;
}

.meta-sep {
  color: var(--text-muted);
  opacity: 0.3;
}

.article-date {
  font-size: 13px;
  color: var(--text-muted);
}

/* 标题 */
.article-title {
  font-size: clamp(28px, 5vw, 44px);
  font-weight: 900;
  letter-spacing: -1.5px;
  line-height: 1.2;
  color: var(--text-primary);
  margin-bottom: 28px;
}

/* 作者区 */
.article-author {
  display: flex;
  align-items: center;
  gap: 16px;
  padding-bottom: 28px;
  margin-bottom: 32px;
  border-bottom: 1px solid var(--border-color, #e8e8e8);
}

.author-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--accent-hover));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 20px;
  flex-shrink: 0;
}

.author-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.author-name {
  font-weight: 700;
  font-size: 15px;
  color: var(--text-primary);
}

.author-bio {
  font-size: 12px;
  color: var(--text-muted);
}

.article-stats {
  margin-left: auto;
  display: flex;
  gap: 16px;
}

.stat-pill {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.stat-num {
  font-size: 20px;
  font-weight: 800;
  color: var(--text-primary);
}

.stat-txt {
  font-size: 10px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* 正文 */
.article-content {
  line-height: 2;
  font-size: 17px;
  color: var(--text-secondary);
}

.article-content :deep(p) {
  margin-bottom: 1.5em;
}

.article-content :deep(strong) {
  color: var(--text-primary);
  font-weight: 700;
}

/* 底部操作 */
.article-footer {
  display: flex;
  gap: 16px;
  margin-top: 48px;
  padding-top: 28px;
  border-top: 1px solid var(--border-color, #e8e8e8);
}

.btn-like {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 32px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--accent), var(--accent-hover));
  color: white;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-like:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255,107,0,0.3);
}

.like-icon {
  font-size: 20px;
}

.btn-back {
  padding: 14px 32px;
  border-radius: 12px;
  border: 2px solid var(--border-color, #ddd);
  color: var(--text-secondary);
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;
  display: flex;
  align-items: center;
  transition: all 0.2s;
}

.btn-back:hover {
  border-color: var(--accent);
  color: var(--accent);
}

/* 侧边栏 */
.article-sidebar {
  padding-top: 20px;
}

.sidebar-card {
  position: sticky;
  top: 80px;
  padding: 24px;
  background: var(--bg-card, white);
  border-radius: 16px;
  border: 1px solid var(--border-color, #eee);
}

.sidebar-card h4 {
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-muted);
  margin-bottom: 16px;
}

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

/* 空状态 */
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

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state a {
  color: var(--accent);
  font-weight: 600;
}

@media (max-width: 900px) {
  .article-body {
    grid-template-columns: 1fr;
    padding: 0 20px 60px;
  }
  .article-hero {
    height: 200px;
  }
  .article-meta-top {
    margin-top: -20px;
  }
  .article-sidebar {
    display: none;
  }
}
</style>
