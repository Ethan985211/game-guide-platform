<template>
  <div class="games-page page">
    <div class="page-header">
      <h1 class="page-title">游戏库</h1>
      <p class="page-subtitle">发现你喜欢的游戏</p>
    </div>

    <div class="search-bar">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="搜索游戏..."
        @keyup.enter="loadGames"
      >
      <button @click="loadGames">搜索</button>
    </div>

    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
    </div>

    <div v-else-if="games.length === 0" class="empty-state">
      <h3>暂无游戏</h3>
      <p>游戏库正在更新中</p>
    </div>

    <div v-else class="games-grid-full">
      <div 
        v-for="game in games" 
        :key="game.id" 
        class="article-card"
        @click="goToGame(game.id)"
      >
        <div class="article-image">
          <img :src="game.cover_image || 'https://picsum.photos/640/400?random=' + game.id" :alt="game.name">
        </div>
        <span class="article-tag">{{ game.category }}</span>
        <h3>{{ game.name }}</h3>
        <p>{{ game.description }}</p>
        <div class="article-meta">
          <span>{{ game.developer }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { gameAPI } from '../api'

const router = useRouter()
const games = ref([])
const searchQuery = ref('')
const loading = ref(false)

const loadGames = async () => {
  loading.value = true
  try {
    const response = await gameAPI.getGames({
      search: searchQuery.value,
      skip: 0,
      limit: 30
    })
    games.value = response.data
  } catch (error) {
    console.error('加载游戏失败', error)
  } finally {
    loading.value = false
  }
}

const goToGame = (id) => router.push(`/games/${id}`)

onMounted(loadGames)
</script>

<style scoped>
.games-grid-full {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

@media (max-width: 1200px) {
  .games-grid-full {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1024px) {
  .games-grid-full {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .games-grid-full {
    grid-template-columns: 1fr;
  }
}
</style>
