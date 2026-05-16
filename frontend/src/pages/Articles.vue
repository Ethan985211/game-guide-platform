<template>
  <div class="articles-page">
    <!-- 页面头部 -->
    <div class="page-hero">
      <h1 class="page-hero-title">攻略文章</h1>
      <p class="page-hero-sub">精选游戏攻略，助你快速上手、轻松通关</p>
      <div class="search-box">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索攻略..."
          class="search-input"
        />
      </div>
      <router-link v-if="isLoggedIn" to="/articles/create" class="btn-create">
        发布攻略
      </router-link>
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
              <span class="author-avatar-sm">{{ (article.author?.username || article.author_name || 'A')[0] }}</span>
              <span>{{ article.author?.username || article.author_name || '管理员' }}</span>
            </div>
            <div class="article-card-stats">
              <span>{{ article.likes || 0 }} 赞</span>
              <span class="meta-sep">·</span>
              <span>{{ article.views || 0 }} 阅读</span>
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

const router = useRouter()
const authStore = useAuthStore()
const articles = ref([])
const loading = ref(true)
const searchQuery = ref('')

const isLoggedIn = computed(() => authStore.isLoggedIn)

const filteredArticles = computed(() => {
  if (!searchQuery.value) return articles.value
  const q = searchQuery.value.toLowerCase()
  return articles.value.filter(a =>
    a.title.toLowerCase().includes(q) ||
    (a.game?.name || a.game_name || '').toLowerCase().includes(q)
  )
})

const extractSummary = (article) => {
  const text = article.content || ''
  return text.replace(/<[^>]*>/g, '').replace(/[*#]/g, '').slice(0, 120) + (text.length > 120 ? '...' : '')
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
  padding: 60px 24px 32px;
  background: var(--bg-primary);
}

.page-hero-title {
  font-size: clamp(32px, 5vw, 48px);
  font-weight: 900;
  letter-spacing: -2px;
  color: var(--text-primary);
  margin-bottom: 10px;
}

.page-hero-sub {
  font-size: 16px;
  color: var(--text-muted);
  margin-bottom: 28px;
}

.search-box {
  max-width: 400px;
  margin: 0 auto 20px;
}

.search-input {
  width: 100%;
  padding: 12px 20px;
  border: 2px solid var(--border-color, #ddd);
  border-radius: 12px;
  font-size: 15px;
  outline: none;
  background: var(--bg-card, white);
  color: var(--text-primary);
  transition: border-color 0.2s;
}

.search-input:focus {
  border-color: var(--accent);
}

.btn-create {
  display: inline-block;
  padding: 12px 32px;
  background: var(--accent);
  color: white;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-create:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255,107,0,0.3);
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
  border-radius: 16px;
  overflow: hidden;
  background: var(--bg-card, white);
  border: 1px solid var(--border-color, #eee);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.article-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 24px 48px rgba(0,0,0,0.1);
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
  transition: transform 0.4s;
}

.article-card:hover .article-card-img img {
  transform: scale(1.05);
}

.article-card-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, transparent 50%);
}

.article-card-overlay {
  position: absolute;
  top: 14px;
  left: 14px;
  right: 14px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.article-card-game {
  padding: 4px 12px;
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(10px);
  border-radius: 8px;
  color: white;
  font-size: 12px;
  font-weight: 700;
}

.article-card-badge {
  padding: 4px 12px;
  background: var(--accent);
  border-radius: 8px;
  color: white;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.article-card-body {
  padding: 24px;
}

.article-card-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.4;
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
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.article-card-author {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-muted);
}

.author-avatar-sm {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--accent);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
}

.article-card-stats {
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  gap: 6px;
}

.meta-sep {
  opacity: 0.3;
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
}
</style>
