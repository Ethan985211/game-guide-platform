<template>
  <div class="game-detail page-container" v-if="game">
    <div class="game-header">
      <img :src="game.cover_image || '/placeholder.png'" class="cover">
      <div class="info">
        <h1>{{ game.name }}</h1>
        <div class="meta">
          <el-tag type="warning">{{ game.category }}</el-tag>
          <span>{{ game.developer }}</span>
          <span>{{ game.publisher }}</span>
        </div>
        <p class="description">{{ game.description }}</p>
      </div>
    </div>

    <section class="section" v-if="characters.length">
      <div class="section-header">
        <h2>角色图鉴</h2>
      </div>
      <div class="card-grid">
        <div v-for="char in characters" :key="char.id" class="character-card">
          <img :src="char.image || '/placeholder.png'" :alt="char.name">
          <div class="char-info">
            <div class="char-name">{{ char.name }}</div>
            <div class="char-tags">
              <el-tag v-if="char.element" size="small" type="warning">{{ char.element }}</el-tag>
              <el-tag v-if="char.weapon_type" size="small">{{ char.weapon_type }}</el-tag>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-header">
        <h2>相关攻略</h2>
      </div>
      <div class="articles-list">
        <div v-for="article in articles" :key="article.id" class="article-card" @click="goToArticle(article.id)">
          <div class="article-card-title">{{ article.title }}</div>
          <div class="article-card-meta">
            <span>{{ article.views }} 阅读</span>
            <span>{{ article.likes }} 点赞</span>
          </div>
        </div>
      </div>
      <el-empty v-if="!articles.length" description="暂无攻略" />
    </section>
  </div>

  <el-skeleton v-else-if="loading" animated />
  <el-empty v-else description="游戏不存在" />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { gameAPI, articleAPI } from '../api'
import analytics from '../utils/analytics'

const route = useRoute()
const router = useRouter()
const game = ref(null)
const characters = ref([])
const articles = ref([])
const loading = ref(false)

const loadData = async () => {
  loading.value = true
  const gameId = route.params.id
  try {
    const [gameRes, charRes, articleRes] = await Promise.all([
      gameAPI.getGame(gameId),
      gameAPI.getGameCharacters(gameId),
      articleAPI.getArticles({ game_id: gameId, limit: 10 })
    ])
    game.value = gameRes.data
    characters.value = charRes.data
    articles.value = articleRes.data
    
    // 记录游戏页面浏览量
    analytics.recordContentView('game', gameId)
  } catch (error) {
    console.error('加载失败', error)
  } finally {
    loading.value = false
  }
}

const goToArticle = (id) => router.push(`/articles/${id}`)

onMounted(loadData)
</script>

<style scoped>
.articles-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
</style>
