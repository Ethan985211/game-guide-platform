<template>
  <div class="articles-page">
    <!-- 页面头部 -->
    <div class="page-hero">
      <h1 class="page-hero-title">攻略文章</h1>
      <p class="page-hero-sub">精选游戏攻略，助你快速上手、轻松通关</p>
      <div class="hero-controls">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索攻略标题或游戏名..."
            class="search-input"
          />
        </div>
        <router-link v-if="isLoggedIn" to="/articles/create" class="btn-create">
          ✏️ 发布攻略
        </router-link>
      </div>
      <!-- 分类标签 -->
      <div class="category-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          class="tab-btn"
          :class="{ active: activeTab === tab.key }"
          @click="activeTab = tab.key"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>

    <!-- 加载 -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 空 -->
    <div v-else-if="filteredArticles.length === 0" class="empty-state">
      <div class="empty-icon">📝</div>
      <h3>暂无攻略</h3>
      <p>成为第一个发布攻略的用户吧</p>
    </div>

    <!-- 列表 -->
    <div v-else class="articles-grid">
      <div
        v-for="article in filteredArticles"
        :key="article.id"
        class="article-card"
        @click="goToArticle(article.id)"
      >
        <div class="article-card-img">
          <img
            v-if="article.cover_image"
            :src="article.cover_image"
            :alt="article.title"
            @error="onImgError"
          />
          <div class="article-card-gradient"></div>
          <div class="article-card-overlay">
            <span class="article-card-game">{{ article.game?.name || article.game_name || '' }}</span>
            <span class="article-card-badge">
              {{ article.category === 'guide' ? '攻略' : article.category === 'tips' ? '心得' : '资讯' }}
            </span>
          </div>
        </div>
        <div class="article-card-body">
          <h3 class="article-card-title">{{ article.title }}</h3>
          <p class="article-card-excerpt">
            {{ extractSummary(article) }}
          </p>
          <div class="article-card-meta">
            <div class="article-card-author">
              <span class="author-avatar-sm" :class="avatarColor(article.author?.username || 'A')">
                {{ (article.author?.username || article.author_name || 'A')[0] }}
              </span>
              <span>{{ article.author?.username || article.author_name || '管理员' }}</span>
            </div>
            <div class="article-card-stats">
              <span class="stat-item">{{ article.views || 0 }} 阅读</span>
              <span class="meta-sep">·</span>
              <span class="stat-item">{{ article.likes || 0 }} 赞</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api'
import { markdownToHtml, htmlToPlainText } from '../utils/markdown.js'

const router = useRouter()
const authStore = useAuthStore()
const articles = ref([])
const loading = ref(true)
const searchQuery = ref('')
const activeTab = ref('all')

const tabs = [
  { key: 'all', label: '全部' },
  { key: 'guide', label: '攻略' },
  { key: 'tips', label: '心得' },
  { key: 'news', label: '资讯' },
]

const isLoggedIn = computed(() => authStore.isLoggedIn)

const filteredArticles = computed(() => {
  let result = articles.value
  if (activeTab.value !== 'all') {
    result = result.filter(a => a.category === activeTab.value)
  }
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(a =>
      a.title.toLowerCase().includes(q) ||
      (a.game?.name || a.game_name || '').toLowerCase().includes(q)
    )
  }
  return result
})

const extractSummary = (article) => {
  const text = article.content || ''
  // Render markdown to HTML first, then strip tags for clean plain text preview
  const html = markdownToHtml(text)
  const plain = htmlToPlainText(html)
  return plain.slice(0, 120) + (plain.length > 120 ? '...' : '')
}

const avatarColor = (name) => {
  const colors = ['avatar-purple', 'avatar-blue', 'avatar-green', 'avatar-orange', 'avatar-pink']
  return colors[(name || 'A').charCodeAt(0) % colors.length]
}

const onImgError = (e) => {
  e.target.style.display = 'none'
}

const goToArticle = (id) => router.push(`/articles/${id}`)

onMounted(async () => {
  try {
    const res = await api.get('/api/articles')
    articles.value = res.data?.items || res.data || []
  } catch (err) {
    console.error('加载文章失败:', err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
/* 页面头部 */
.page-hero {
  text-align: center;
  padding: 72px 24px 32px;
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border-color, #eee);
}

.page-hero-title {
  font-size: clamp(36px, 6vw, 56px);
  font-weight: 900;
  letter-spacing: -2px;
  color: var(--text-primary);
  margin-bottom: 10px;
}

.page-hero-sub {
  font-size: 17px;
  color: var(--text-muted);
  margin-bottom: 32px;
}

.hero-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-bottom: 28px;
}

/* 搜索框 */
.search-box {
  position: relative;
  max-width: 420px;
  width: 100%;
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 16px;
  opacity: 0.5;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 14px 20px 14px 44px;
  border: 2px solid var(--border-color, #ddd);
  border-radius: 14px;
  font-size: 15px;
  outline: none;
  background: var(--bg-card, white);
  color: var(--text-primary);
  transition: border-color 0.25s, box-shadow 0.25s;
}

.search-input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 4px rgba(255,107,0,0.1);
}

.search-input::placeholder {
  color: var(--text-muted);
  opacity: 0.5;
}

.btn-create {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 14px 28px;
  background: var(--accent);
  color: white;
  border-radius: 14px;
  font-size: 15px;
  font-weight: 700;
  text-decoration: none;
  transition: transform 0.2s, box-shadow 0.2s;
  flex-shrink: 0;
}

.btn-create:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255,107,0,0.3);
}

/* 分类标签 */
.category-tabs {
  display: flex;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 10px 24px;
  border: 2px solid var(--border-color, #ddd);
  border-radius: 100px;
  background: var(--bg-card, white);
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.tab-btn.active {
  background: var(--accent);
  border-color: var(--accent);
  color: white;
}

/* 文章网格 */
.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 28px;
  padding: 48px;
  max-width: 1300px;
  margin: 0 auto;
}

.article-card {
  border-radius: 18px;
  overflow: hidden;
  background: var(--bg-card, white);
  border: 1px solid var(--border-color, #eee);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.article-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 28px 56px rgba(0,0,0,0.1);
}

.article-card-img {
  position: relative;
  aspect-ratio: 16/10;
  background: var(--bg-dark);
  overflow: hidden;
}

.article-card-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.article-card:hover .article-card-img img {
  transform: scale(1.06);
}

.article-card-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, transparent 50%);
}

.article-card-overlay {
  position: absolute;
  top: 16px;
  left: 16px;
  right: 16px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.article-card-game {
  padding: 6px 14px;
  background: rgba(255,255,255,0.16);
  backdrop-filter: blur(12px);
  border-radius: 8px;
  color: white;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.3px;
}

.article-card-badge {
  padding: 6px 14px;
  background: var(--accent);
  border-radius: 8px;
  color: white;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1px;
}

.article-card-body {
  padding: 24px;
}

.article-card-title {
  font-size: 18px;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1.45;
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-card-excerpt {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 18px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid var(--border-color, #f0f0f0);
}

.article-card-author {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 500;
}

.author-avatar-sm {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  color: white;
}

.avatar-purple { background: linear-gradient(135deg, #667eea, #764ba2); }
.avatar-blue { background: linear-gradient(135deg, #4facfe, #00f2fe); }
.avatar-green { background: linear-gradient(135deg, #43e97b, #38f9d7); }
.avatar-orange { background: linear-gradient(135deg, #fa709a, #fee140); }
.avatar-pink { background: linear-gradient(135deg, #f093fb, #f5576c); }

.article-card-stats {
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  gap: 4px;
}

.stat-item {
  color: var(--text-muted);
}

.meta-sep {
  opacity: 0.3;
  margin: 0 4px;
}

/* 状态 */
.loading-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  gap: 16px;
  color: var(--text-muted);
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

.empty-icon { font-size: 48px; }
.empty-state h3 { color: var(--text-primary); font-size: 20px; }

@media (max-width: 768px) {
  .articles-grid {
    padding: 24px 20px;
    grid-template-columns: 1fr;
  }
  .page-hero {
    padding: 48px 20px 24px;
  }
  .hero-controls {
    flex-direction: column;
  }
  .search-box {
    max-width: 100%;
  }
  .btn-create {
    width: 100%;
    justify-content: center;
  }
}
</style>
