<template>
  <div class="games-page">
    <!-- 页面头部 -->
    <div class="page-hero">
      <h1 class="page-hero-title">游戏库</h1>
      <p class="page-hero-sub">探索热门游戏，发现你的下一款挚爱</p>
      <div class="search-box">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索游戏名称..."
          @keyup.enter="loadGames"
          class="search-input"
        />
        <button @click="loadGames" class="search-btn">搜索</button>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 空状态 -->
    <div v-else-if="games.length === 0" class="empty-state">
      <div class="empty-icon">🎮</div>
      <h3>暂无游戏</h3>
      <p>游戏库正在更新中，稍后再来看看</p>
    </div>

    <!-- 游戏网格 -->
    <div v-else class="games-grid">
      <div
        v-for="game in games"
        :key="game.id"
        class="game-card"
        @click="goToGame(game.id)"
      >
        <div class="game-card-img">
          <div class="game-card-gradient" :style="gradientBg(game.id)"></div>
          <img
            v-if="game.cover_image"
            :src="game.cover_image"
            :alt="game.name"
            @error="onImgError"
            class="game-card-cover"
          />
          <div class="game-card-img-overlay"></div>
          <span class="game-card-cat-badge">{{ game.category }}</span>
        </div>
        <div class="game-card-body">
          <h3 class="game-card-name">{{ game.name }}</h3>
          <p class="game-card-desc">{{ game.description?.slice(0, 80) }}{{ game.description?.length > 80 ? '...' : '' }}</p>
          <div class="game-card-footer">
            <span class="game-card-dev">{{ game.developer }}</span>
            <span class="game-card-arrow">→</span>
          </div>
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
const loading = ref(true)

const gradientBg = (id) => {
  const gradients = [
    'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
    'linear-gradient(135deg, #2d1b69 0%, #1b1438 50%, #0d0d2b 100%)',
    'linear-gradient(135deg, #1b4332 0%, #081c15 100%)',
    'linear-gradient(135deg, #3a1c71 0%, #d76d77 50%, #ffaf7b 100%)',
    'linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%)',
    'linear-gradient(135deg, #200122 0%, #6f0000 100%)',
    'linear-gradient(135deg, #000428 0%, #004e92 100%)',
  ]
  return { background: gradients[(id - 1) % gradients.length] }
}

const onImgError = (e) => {
  e.target.style.display = 'none'
}

const goToGame = (id) => router.push(`/games/${id}`)

const loadGames = async () => {
  loading.value = true
  try {
    const response = await gameAPI.getGames({
      search: searchQuery.value,
      skip: 0,
      limit: 30
    })
    games.value = response.data?.items || response.data || []
  } catch (error) {
    console.error('加载游戏失败', error)
  } finally {
    loading.value = false
  }
}

onMounted(loadGames)
</script>

<style scoped>
/* 页面头部 */
.page-hero {
  text-align: center;
  padding: 80px 24px 48px;
  background: var(--bg-primary);
}

.page-hero-title {
  font-size: clamp(36px, 6vw, 56px);
  font-weight: 900;
  letter-spacing: -2px;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.page-hero-sub {
  font-size: 17px;
  color: var(--text-muted);
  margin-bottom: 36px;
}

.search-box {
  display: flex;
  max-width: 480px;
  margin: 0 auto;
  gap: 0;
}

.search-input {
  flex: 1;
  padding: 14px 20px;
  border: 2px solid var(--border-color, #ddd);
  border-right: none;
  border-radius: 12px 0 0 12px;
  font-size: 15px;
  outline: none;
  transition: border-color 0.2s;
  background: var(--bg-card, white);
  color: var(--text-primary);
}

.search-input:focus {
  border-color: var(--accent);
}

.search-btn {
  padding: 14px 28px;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 0 12px 12px 0;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
}

.search-btn:hover {
  background: var(--accent-hover);
}

/* 游戏网格 */
.games-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 28px;
  padding: 48px;
  max-width: 1300px;
  margin: 0 auto;
}

.game-card {
  border-radius: 18px;
  overflow: hidden;
  background: var(--bg-card, white);
  border: 1px solid var(--border-color, #eee);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.game-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 28px 56px rgba(0,0,0,0.14);
}

.game-card-img {
  position: relative;
  aspect-ratio: 16/10;
  overflow: hidden;
}

.game-card-gradient {
  position: absolute;
  inset: 0;
}

.game-card-cover {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.game-card:hover .game-card-cover {
  transform: scale(1.08);
}

.game-card-img-overlay {
  position: absolute;
  inset: 0;
  z-index: 2;
  background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, transparent 60%);
}

.game-card-cat-badge {
  position: absolute;
  top: 14px;
  left: 14px;
  z-index: 3;
  padding: 5px 12px;
  border-radius: 8px;
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(10px);
  color: white;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.game-card-body {
  padding: 24px;
  position: relative;
  z-index: 3;
  margin-top: -24px;
  background: var(--bg-card, white);
  border-radius: 24px 24px 0 0;
}

.game-card-name {
  font-size: 22px;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 10px;
  letter-spacing: -0.5px;
}

.game-card-desc {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 16px;
}

.game-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.game-card-dev {
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 600;
}

.game-card-arrow {
  font-size: 18px;
  color: var(--text-muted);
  transition: transform 0.3s, color 0.3s;
}

.game-card:hover .game-card-arrow {
  transform: translateX(4px);
  color: var(--accent);
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

.empty-icon {
  font-size: 48px;
}

.empty-state h3 {
  font-size: 20px;
  color: var(--text-primary);
}

@media (max-width: 768px) {
  .games-grid {
    padding: 24px 20px;
    grid-template-columns: 1fr;
  }
  .page-hero {
    padding: 60px 20px 32px;
  }
}
</style>
