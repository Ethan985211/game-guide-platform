<template>
  <div class="articles-page page">
    <div class="page-header">
      <h1 class="page-title">攻略文章</h1>
      <p class="page-subtitle">精选游戏攻略，助你快速上手</p>
    </div>

    <div class="search-bar">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="搜索攻略..."
        @keyup.enter="handleSearch"
      >
      <button @click="handleSearch">搜索</button>
    </div>

    <router-link v-if="isLoggedIn" to="/articles/create" class="create-btn">
      发布攻略
    </router-link>

    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
    </div>

    <div v-else-if="filteredArticles.length === 0" class="empty-state">
      <h3>暂无攻略</h3>
      <p>成为第一个发布攻略的用户吧</p>
    </div>

    <div v-else class="articles-grid-full">
      <div 
        v-for="article in filteredArticles" 
        :key="article.id" 
        class="article-card"
        @click="goToArticle(article.id)"
      >
        <div class="article-image">
          <img :src="article.cover_image || 'https://picsum.photos/640/400?random=' + article.id" :alt="article.title">
        </div>
        <span class="article-tag">{{ article.game_name }}</span>
        <h3>{{ article.title }}</h3>
        <p>{{ article.summary || article.content?.slice(0, 100) }}...</p>
        <div class="article-meta">
          <span>{{ article.author_name }}</span>
          <span>{{ article.likes || 0 }} 点赞</span>
          <span>{{ article.comment_count || 0 }} 评论</span>
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
  const query = searchQuery.value.toLowerCase()
  return articles.value.filter(article => 
    article.title.toLowerCase().includes(query) ||
    article.game_name?.toLowerCase().includes(query)
  )
})

const goToArticle = (id) => router.push(`/articles/${id}`)
const handleSearch = () => {}

onMounted(async () => {
  try {
    const res = await api.get('/api/articles')
    articles.value = res.data
  } catch (err) {
    console.error('加载文章失败:', err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.create-btn {
  display: inline-block;
  padding: 14px 28px;
  background: var(--accent);
  color: white;
  font-weight: 700;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 1px;
  border-radius: 4px;
  margin-bottom: 32px;
  transition: background 0.2s;
}

.create-btn:hover {
  background: var(--accent-hover);
}

.articles-grid-full {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}

@media (max-width: 1024px) {
  .articles-grid-full {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .articles-grid-full {
    grid-template-columns: 1fr;
  }
}
</style>
