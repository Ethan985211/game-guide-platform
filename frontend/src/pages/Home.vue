<template>
  <div class="home">
    <!-- 英雄区域 -->
    <section class="hero" @mousemove="handleHeroMouseMove" @mouseleave="handleHeroMouseLeave">
      <!-- 背景擦除交互 -->
      <GlassWipe class="hero-wipe" :mouse-x="heroMouseX" :mouse-y="heroMouseY" />
      
      <div class="hero-content">
        <h1>发现游戏世界<br><span class="highlight">无限精彩</span></h1>
        <p>最全的游戏攻略，最深的角色解析，最热的社区讨论</p>
        <div class="hero-buttons">
          <router-link to="/games"><button class="btn-explore">探索游戏</button></router-link>
        </div>
      </div>
    </section>

    <!-- 统计 -->
    <section class="stats">
      <div class="stat-item">
        <div class="stat-number">{{ games.length }}+</div>
        <div class="stat-label">热门游戏</div>
      </div>
      <div class="stat-item">
        <div class="stat-number">{{ articles.length }}+</div>
        <div class="stat-label">攻略文章</div>
      </div>
    </section>

    <!-- 游戏推荐 -->
    <section class="section">
      <div class="section-header">
        <h2 class="section-title">热门游戏</h2>
        <router-link to="/games" class="section-link">查看全部 →</router-link>
      </div>
      <div class="games-grid">
        <div 
          v-for="game in games.slice(0, 4)" 
          :key="game.id" 
          class="game-card"
          @click="goToGame(game.id)"
        >
          <img :src="game.image || 'https://picsum.photos/400/600?random=' + game.id" :alt="game.name">
          <div class="game-card-overlay">
            <h3>{{ game.name }}</h3>
            <p>{{ game.category }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 最新攻略 -->
    <section class="section">
      <div class="section-header">
        <h2 class="section-title">最新攻略</h2>
        <router-link to="/articles" class="section-link">查看全部 →</router-link>
      </div>
      <div class="articles-grid">
        <div 
          v-for="article in articles.slice(0, 3)" 
          :key="article.id" 
          class="article-card"
          @click="goToArticle(article.id)"
        >
          <div class="article-image">
            <img :src="article.cover_image || 'https://picsum.photos/640/400?random=' + article.id" :alt="article.title">
          </div>
          <div class="article-content">
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
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import GlassWipe from '../components/GlassWipe.vue'

const router = useRouter()
const games = ref([])
const articles = ref([])
const heroMouseX = ref(-1000)
const heroMouseY = ref(-1000)
const globalMouseX = ref(0)
const globalMouseY = ref(0)
const isMouseInHero = ref(false)

const goToGame = (id) => router.push(`/games/${id}`)
const goToArticle = (id) => router.push(`/articles/${id}`)

const handleHeroMouseMove = (e) => {
  globalMouseX.value = e.clientX
  globalMouseY.value = e.clientY
  isMouseInHero.value = true
  updateHeroMousePosition()
}

const handleHeroMouseLeave = () => {
  isMouseInHero.value = false
  heroMouseX.value = -1000
  heroMouseY.value = -1000
}

const updateHeroMousePosition = () => {
  if (!isMouseInHero.value) return
  const hero = document.querySelector('.hero')
  if (hero) {
    const rect = hero.getBoundingClientRect()
    heroMouseX.value = globalMouseX.value - rect.left
    heroMouseY.value = globalMouseY.value - rect.top
  }
}

onMounted(async () => {
  window.addEventListener('mousemove', (e) => {
    globalMouseX.value = e.clientX
    globalMouseY.value = e.clientY
  })
  
  try {
    const [gamesRes, articlesRes] = await Promise.all([
      api.get('/api/games'),
      api.get('/api/articles')
    ])
    games.value = gamesRes.data
    articles.value = articlesRes.data
  } catch (err) {
    console.error('加载数据失败:', err)
  }
})
</script>

<style scoped>
.home {
  position: relative;
}

/* 英雄区域 - 超大字标题 */
.hero {
  position: relative;
  min-height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
  overflow: hidden;
  padding: 80px 24px;
}

.hero-wipe {
  position: absolute;
  inset: 0;
  z-index: 1;
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 900px;
}

/* 杂志封面式大标题 */
.hero h1 {
  font-size: clamp(56px, 10vw, 100px);
  font-weight: 900;
  line-height: 0.95;
  letter-spacing: -4px;
  margin-bottom: 32px;
  color: var(--text-primary);
}

.hero h1 .highlight {
  color: var(--accent);
  display: block;
}

.hero p {
  font-size: 22px;
  color: var(--text-secondary);
  margin-bottom: 48px;
  line-height: 1.6;
}

/* 简洁按钮 */
.hero-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.btn-explore,
.btn-join {
  padding: 20px 56px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-decoration: none;
  display: inline-block;
}

.btn-explore {
  background: var(--accent);
  color: white;
  border: none;
  box-shadow: 0 4px 16px rgba(255, 107, 0, 0.3);
}

.btn-explore:hover {
  background: var(--accent-hover);
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(255, 107, 0, 0.4);
}

.btn-join {
  background: transparent;
  color: var(--text-primary);
  border: 2px solid var(--border-dark);
}

.btn-join:hover {
  border-color: var(--text-primary);
  transform: translateY(-3px);
}

/* 统计区域 */
.stats {
  display: flex;
  justify-content: center;
  gap: 100px;
  padding: 80px 24px;
  background: white;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 48px;
  font-weight: 900;
  color: var(--text-primary);
  letter-spacing: -2px;
}

.stat-label {
  font-size: 13px;
  color: var(--text-muted);
  margin-top: 8px;
  text-transform: uppercase;
  letter-spacing: 2px;
}

/* 区块 */
.section {
  padding: 80px 0;
  background: var(--bg-primary);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 48px;
  padding: 0 48px;
}

.section-title {
  font-size: 40px;
  font-weight: 900;
  letter-spacing: -2px;
  color: var(--text-primary);
  position: relative;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -12px;
  left: 0;
  width: 60px;
  height: 4px;
  background: var(--accent);
}

.section-link {
  color: var(--accent);
  text-decoration: none;
  font-size: 14px;
  font-weight: 700;
}

.section-link:hover {
  color: var(--accent-hover);
}

/* 游戏卡片 - 黑白底 + 悬停缩放 */
.games-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  padding: 0 48px;
}

.game-card {
  position: relative;
  aspect-ratio: 3/4;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  background: var(--bg-dark);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: var(--shadow-sm);
}

.game-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: var(--shadow-lg);
}

.game-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.game-card:hover img {
  transform: scale(1.1);
}

.game-card-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 24px;
  background: linear-gradient(to top, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0.6) 50%, transparent 100%);
}

.game-card h3 {
  font-size: 20px;
  font-weight: 800;
  color: white;
  margin-bottom: 6px;
  letter-spacing: -0.5px;
}

.game-card p {
  font-size: 11px;
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: 2px;
  font-weight: 600;
}

/* 最新攻略 */
.articles-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  padding: 0 48px;
}

.article-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: var(--shadow-sm);
}

.article-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-md);
}

.article-image {
  aspect-ratio: 16/10;
  overflow: hidden;
}

.article-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s;
}

.article-card:hover .article-image img {
  transform: scale(1.05);
}

.article-content {
  padding: 24px;
}

.article-tag {
  display: inline-block;
  padding: 6px 12px;
  background: var(--accent-light);
  color: var(--accent);
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  border-radius: 6px;
  margin-bottom: 16px;
}

.article-card h3 {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 12px;
  line-height: 1.4;
  transition: color 0.2s;
}

.article-card:hover h3 {
  color: var(--accent);
}

.article-card p {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 20px;
}

.article-meta {
  display: flex;
  gap: 20px;
  font-size: 12px;
  color: var(--text-muted);
}

/* 响应式 */
@media (max-width: 1024px) {
  .games-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .articles-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .hero {
    min-height: 500px;
    padding: 60px 20px;
  }
  
  .hero h1 {
    letter-spacing: -2px;
  }
  
  .hero-buttons {
    flex-direction: column;
    gap: 16px;
  }
  
  .btn-explore, .btn-join {
    width: 100%;
    text-align: center;
  }
  
  .stats {
    gap: 48px;
    padding: 60px 24px;
  }
  
  .stat-number {
    font-size: 36px;
  }
  
  .section-header {
    padding: 0 20px;
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .section-title {
    font-size: 32px;
  }
  
  .games-grid,
  .articles-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    padding: 0 20px;
  }
}

@media (max-width: 480px) {
  .games-grid,
  .articles-grid {
    grid-template-columns: 1fr;
  }
  
  .hero h1 {
    font-size: 42px;
    letter-spacing: -1px;
  }
  
  .stat-number {
    font-size: 32px;
  }
}
</style>
