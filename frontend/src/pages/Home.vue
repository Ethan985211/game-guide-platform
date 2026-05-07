<template>
  <div class="home page-container">
    <!-- 搜索区域 -->
    <div class="search-section">
      <el-input
        v-model="searchQuery"
        placeholder="搜索游戏、文章、角色..."
        size="large"
        @keyup.enter="handleSearch"
      >
        <template #append>
          <el-button :icon="Search" @click="handleSearch" />
        </template>
      </el-input>
    </div>

    <!-- 搜索结果 -->
    <div v-if="searchResults" class="search-results">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="游戏" name="games">
          <div class="card-grid">
            <div v-for="game in searchResults.games" :key="game.id" class="game-card" @click="goToGame(game.id)">
              <img :src="game.cover_image || '/placeholder.png'" :alt="game.name">
              <div class="game-card-content">
                <div class="game-card-title">{{ game.name }}</div>
                <div class="game-card-desc">{{ game.description }}</div>
              </div>
            </div>
          </div>
          <el-empty v-if="!searchResults.games?.length" description="暂无游戏" />
        </el-tab-pane>
        <el-tab-pane label="文章" name="articles">
          <div v-for="article in searchResults.articles" :key="article.id" class="article-card" @click="goToArticle(article.id)">
            <div class="article-card-title">{{ article.title }}</div>
            <div class="article-card-meta">
              <span>浏览 {{ article.views }}</span>
              <span>点赞 {{ article.likes }}</span>
              <span>{{ formatDate(article.created_at) }}</span>
            </div>
          </div>
          <el-empty v-if="!searchResults.articles?.length" description="暂无文章" />
        </el-tab-pane>
        <el-tab-pane label="角色" name="characters">
          <div class="card-grid">
            <div v-for="char in searchResults.characters" :key="char.id" class="game-card">
              <img :src="char.image || '/placeholder.png'" :alt="char.name">
              <div class="game-card-content">
                <div class="game-card-title">{{ char.name }}</div>
                <div class="game-card-desc">{{ char.element }} · {{ char.weapon_type }}</div>
              </div>
            </div>
          </div>
          <el-empty v-if="!searchResults.characters?.length" description="暂无角色" />
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 首页内容 -->
    <div v-else>
      <!-- 最新游戏 -->
      <section class="section">
        <div class="section-header">
          <h2>热门游戏</h2>
          <router-link to="/games" class="more-link">查看更多 →</router-link>
        </div>
        <div class="card-grid">
          <div v-for="game in games" :key="game.id" class="game-card" @click="goToGame(game.id)">
            <img :src="game.cover_image || '/placeholder.png'" :alt="game.name">
            <div class="game-card-content">
              <div class="game-card-title">{{ game.name }}</div>
              <div class="game-card-desc">{{ game.description }}</div>
            </div>
          </div>
        </div>
      </section>

      <!-- 最新攻略 -->
      <section class="section">
        <div class="section-header">
          <h2>最新攻略</h2>
          <router-link to="/articles" class="more-link">查看更多 →</router-link>
        </div>
        <div class="articles-list">
          <div v-for="article in articles" :key="article.id" class="article-card" @click="goToArticle(article.id)">
            <div class="article-card-title">{{ article.title }}</div>
            <div class="article-card-meta">
              <span>作者: {{ article.author?.username }}</span>
              <span>浏览 {{ article.views }}</span>
              <span>点赞 {{ article.likes }}</span>
              <span>{{ formatDate(article.created_at) }}</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search } from '@element-plus/icons-vue'
import { gameAPI, articleAPI, searchAPI } from '../api'

const router = useRouter()
const searchQuery = ref('')
const searchResults = ref(null)
const activeTab = ref('games')
const games = ref([])
const articles = ref([])

const loadData = async () => {
  try {
    const [gamesRes, articlesRes] = await Promise.all([
      gameAPI.getGames({ limit: 8 }),
      articleAPI.getArticles({ limit: 10 })
    ])
    games.value = gamesRes.data
    articles.value = articlesRes.data
  } catch (error) {
    console.error('加载数据失败', error)
  }
}

const handleSearch = async () => {
  if (!searchQuery.value.trim()) return
  try {
    const response = await searchAPI.search(searchQuery.value)
    searchResults.value = response.data
  } catch (error) {
    console.error('搜索失败', error)
  }
}

const goToGame = (id) => router.push(`/games/${id}`)
const goToArticle = (id) => router.push(`/articles/${id}`)
const formatDate = (date) => new Date(date).toLocaleDateString('zh-CN')

onMounted(loadData)
</script>

<style scoped>
.home {
  padding-top: 20px;
}

.search-section {
  max-width: 600px;
  margin: 0 auto 40px;
}

.section {
  margin-bottom: 40px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  font-size: 22px;
  color: #303133;
}

.more-link {
  color: #409eff;
  font-size: 14px;
}

.search-results {
  background: white;
  border-radius: 12px;
  padding: 20px;
  min-height: 400px;
}

.articles-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>
