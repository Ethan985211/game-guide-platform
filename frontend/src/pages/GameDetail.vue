<template>
  <div class="game-detail page-container" v-if="game">
    <!-- 游戏信息 -->
    <div class="game-header">
      <img :src="game.cover_image || '/placeholder.png'" class="cover">
      <div class="info">
        <h1>{{ game.name }}</h1>
        <div class="meta">
          <el-tag>{{ game.category }}</el-tag>
          <span>开发商: {{ game.developer }}</span>
          <span>发行商: {{ game.publisher }}</span>
        </div>
        <p class="description">{{ game.description }}</p>
      </div>
    </div>

    <!-- 角色列表 -->
    <section class="section" v-if="characters.length">
      <h2>角色图鉴</h2>
      <div class="card-grid">
        <div v-for="char in characters" :key="char.id" class="character-card">
          <img :src="char.image || '/placeholder.png'" :alt="char.name">
          <div class="char-info">
            <div class="char-name">{{ char.name }}</div>
            <div class="char-tags">
              <el-tag v-if="char.element" size="small">{{ char.element }}</el-tag>
              <el-tag v-if="char.weapon_type" size="small" type="info">{{ char.weapon_type }}</el-tag>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 相关攻略 -->
    <section class="section">
      <h2>相关攻略</h2>
      <div class="articles-list">
        <div v-for="article in articles" :key="article.id" class="article-card" @click="goToArticle(article.id)">
          <div class="article-card-title">{{ article.title }}</div>
          <div class="article-card-meta">
            <span>浏览 {{ article.views }}</span>
            <span>点赞 {{ article.likes }}</span>
          </div>
        </div>
      </div>
      <el-empty v-if="!articles.length" description="暂无攻略" />
    </section>
  </div>

  <el-skeleton v-else-if="loading" />
  <el-empty v-else description="游戏不存在" />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { gameAPI, articleAPI } from '../api'

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
.game-header {
  display: flex;
  gap: 24px;
  background: white;
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 32px;
}

.cover {
  width: 280px;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
}

.info h1 {
  font-size: 28px;
  margin-bottom: 12px;
}

.meta {
  display: flex;
  gap: 16px;
  align-items: center;
  margin-bottom: 16px;
  color: #606266;
}

.description {
  color: #606266;
  line-height: 1.6;
}

.section {
  margin-bottom: 32px;
}

.section h2 {
  font-size: 20px;
  margin-bottom: 16px;
}

.character-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  text-align: center;
}

.character-card img {
  width: 100%;
  height: 120px;
  object-fit: cover;
}

.char-info {
  padding: 12px;
}

.char-name {
  font-weight: 600;
  margin-bottom: 8px;
}

.char-tags {
  display: flex;
  gap: 4px;
  justify-content: center;
}

.articles-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
</style>
