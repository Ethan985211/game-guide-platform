<template>
  <div class="games page-container">
    <h1 class="page-title">游戏库</h1>

    <!-- 筛选 -->
    <div class="filters">
      <el-input
        v-model="searchQuery"
        placeholder="搜索游戏..."
        clearable
        style="width: 300px"
        @change="loadGames"
      />
      <el-select v-model="category" placeholder="游戏类型" clearable @change="loadGames">
        <el-option label="RPG" value="RPG" />
        <el-option label="FPS" value="FPS" />
        <el-option label="MOBA" value="MOBA" />
        <el-option label="SLG" value="SLG" />
        <el-option label="休闲" value="休闲" />
      </el-select>
    </div>

    <!-- 游戏列表 -->
    <div class="card-grid">
      <div v-for="game in games" :key="game.id" class="game-card" @click="goToGame(game.id)">
        <img :src="game.cover_image || '/placeholder.png'" :alt="game.name">
        <div class="game-card-content">
          <div class="game-card-title">{{ game.name }}</div>
          <div class="game-card-meta">
            <el-tag size="small">{{ game.category }}</el-tag>
            <span class="developer">{{ game.developer }}</span>
          </div>
          <div class="game-card-desc">{{ game.description }}</div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="20"
        :total="total"
        layout="prev, pager, next"
        @current-change="loadGames"
      />
    </div>

    <el-empty v-if="!games.length && !loading" description="暂无游戏" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { gameAPI } from '../api'

const router = useRouter()
const games = ref([])
const searchQuery = ref('')
const category = ref('')
const currentPage = ref(1)
const total = ref(0)
const loading = ref(false)

const loadGames = async () => {
  loading.value = true
  try {
    const response = await gameAPI.getGames({
      search: searchQuery.value,
      category: category.value,
      skip: (currentPage.value - 1) * 20,
      limit: 20
    })
    games.value = response.data
    total.value = response.data.length
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
.games {
  padding-top: 20px;
}

.filters {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.game-card-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.developer {
  font-size: 12px;
  color: #909399;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}
</style>
