<template>
  <div class="home">
    <!-- 英雄区域 -->
    <section class="hero" @mousemove="handleHeroMouseMove" @mouseleave="handleHeroMouseLeave">
      <GlassWipe class="hero-wipe" :mouse-x="heroMouseX" :mouse-y="heroMouseY" />
      <div class="hero-bg-pattern"></div>
      <div class="hero-content">
        <div class="hero-badge">GAME GUIDE PLATFORM</div>
        <h1>发现游戏世界<br><span class="highlight">无限精彩</span></h1>
        <p>最全的游戏攻略，最深的角色解析，最热的社区讨论</p>
        <div class="hero-actions">
          <router-link to="/games" class="btn-primary">探索游戏</router-link>
          <router-link to="/articles" class="btn-secondary">浏览攻略</router-link>
        </div>
      </div>
      <div class="hero-scroll-hint">
        <span></span>
      </div>
    </section>

    <!-- 数据统计 -->
    <section class="stats-bar">
      <div class="stat-card">
        <span class="stat-number">{{ games.length }}</span>
        <span class="stat-label">热门游戏</span>
        <span class="stat-accent"></span>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-card">
        <span class="stat-number">{{ articles.length }}</span>
        <span class="stat-label">攻略文章</span>
        <span class="stat-accent"></span>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-card">
        <span class="stat-number">{{ totalViews }}</span>
        <span class="stat-label">总浏览量</span>
        <span class="stat-accent"></span>
      </div>
    </section>

    <!-- 推广卡片 -->
    <div class="section">
      <PromoCard />
    </div>

    <!-- 热门游戏 -->
    <section class="section section-games">
      <div class="section-header">
        <div>
          <h2 class="section-title">热门游戏</h2>
          <p class="section-subtitle">精选最受欢迎的游戏，总有你喜欢的</p>
        </div>
        <router-link to="/games" class="section-link">
          查看全部 <span class="link-arrow">→</span>
        </router-link>
      </div>
      <div class="games-grid">
        <div
          v-for="game in games.slice(0, 6)"
          :key="game.id"
          class="game-card"
          @click="goToGame(game.id)"
        >
          <div class="game-card-img">
            <div class="game-card-bg" :style="gradientBg(game.id)"></div>
            <img
              v-if="game.cover_image"
              :src="game.cover_image"
              :alt="game.name"
              @error="onImgError"
              class="game-card-cover"
            />
            <div class="game-card-overlay"></div>
          </div>
          <div class="game-card-body">
            <span class="game-card-cat">{{ game.category }}</span>
            <h3 class="game-card-title">{{ game.name }}</h3>
            <p class="game-card-desc">{{ game.description?.slice(0, 60) }}{{ game.description?.length > 60 ? '...' : '' }}</p>
            <div class="game-card-footer">
              <span class="game-card-dev">{{ game.developer }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 最新攻略 -->
    <section class="section section-articles">
      <div class="section-header">
        <div>
          <h2 class="section-title">最新攻略</h2>
          <p class="section-subtitle">热门游戏攻略、角色解析、上分心得</p>
        </div>
        <router-link to="/articles" class="section-link">
          查看全部 <span class="link-arrow">→</span>
        </router-link>
      </div>
      <div class="articles-grid">
        <div
          v-for="article in articles.slice(0, 6)"
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
            <span class="article-card-badge">
              {{ article.category === 'guide' ? '攻略' : article.category === 'tips' ? '心得' : '资讯' }}
            </span>
          </div>
          <div class="article-card-body">
            <span class="article-card-game">{{ article.game?.name || article.game_name || '游戏攻略' }}</span>
            <h3 class="article-card-title">{{ article.title }}</h3>
            <p class="article-card-excerpt">
              {{ extractSummary(article) }}
            </p>
            <div class="article-card-meta">
              <span>{{ article.author?.username || article.author_name || '管理员' }}</span>
              <span class="meta-dot">·</span>
              <span>{{ article.likes || 0 }} 赞</span>
              <span class="meta-dot">·</span>
              <span>{{ article.views || 0 }} 阅读</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import GlassWipe from '../components/GlassWipe.vue'
import PromoCard from '../components/PromoCard.vue'

const router = useRouter()
const games = ref([])
const articles = ref([])
const heroMouseX = ref(-1000)
const heroMouseY = ref(-1000)
const globalMouseX = ref(0)
const globalMouseY = ref(0)
const isMouseInHero = ref(false)

const totalViews = computed(() => {
  return articles.value.reduce((sum, a) => sum + (a.views || 0), 0)
})

const gradientBg = (id) => {
  const gradients = [
    'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    'linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)',
    'linear-gradient(135deg, #fccb90 0%, #d57eeb 100%)',
  ]
  return { background: gradients[(id - 1) % gradients.length] }
}

const extractSummary = (article) => {
  const text = article.content || ''
  const clean = text.replace(/<[^>]*>/g, '').replace(/\*\*/g, '').replace(/#/g, '')
  return clean.slice(0, 100) + (clean.length > 100 ? '...' : '')
}

const onImgError = (e) => {
  e.target.style.display = 'none'
}

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

const onGlobalMouseMove = (e) => {
  globalMouseX.value = e.clientX
  globalMouseY.value = e.clientY
}

onMounted(async () => {
  window.addEventListener('mousemove', onGlobalMouseMove)

  try {
    const [gamesRes, articlesRes] = await Promise.all([
      api.get('/api/games'),
      api.get('/api/articles')
    ])
    games.value = gamesRes.data?.items || gamesRes.data || []
    articles.value = articlesRes.data?.items || articlesRes.data || []
  } catch (err) {
    console.error('加载数据失败:', err)
  }
})

onUnmounted(() => {
  window.removeEventListener('mousemove', onGlobalMouseMove)
})
</script>

<style scoped>
/* ===================== 英雄区域 ===================== */
.hero {
  position: relative;
  min-height: 85vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-primary);
  overflow: hidden;
  padding: 120px 24px 80px;
}

.hero-bg-pattern {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 50% -20%, rgba(255,107,0,0.08), transparent),
    radial-gradient(ellipse 50% 50% at 80% 80%, rgba(100,100,255,0.06), transparent);
  z-index: 0;
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
  max-width: 800px;
}

.hero-badge {
  display: inline-block;
  padding: 8px 20px;
  border-radius: 100px;
  border: 1px solid var(--border-color, #ddd);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 3px;
  color: var(--text-muted);
  margin-bottom: 32px;
}

.hero h1 {
  font-size: clamp(64px, 10vw, 120px);
  font-weight: 900;
  line-height: 1.0;
  letter-spacing: -3px;
  margin-bottom: 20px;
  color: var(--text-primary);
}

.hero h1 .highlight {
  background: linear-gradient(135deg, var(--accent), #ff4444);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero p {
  font-size: 20px;
  color: var(--text-secondary);
  margin-bottom: 48px;
  line-height: 1.7;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.btn-primary {
  padding: 18px 40px;
  border-radius: 12px;
  background: var(--accent);
  color: white;
  font-size: 16px;
  font-weight: 700;
  text-decoration: none;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 4px 20px rgba(255,107,0,0.3);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(255,107,0,0.4);
}

.btn-secondary {
  padding: 18px 40px;
  border-radius: 12px;
  border: 2px solid var(--border-color, #ddd);
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-secondary:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.hero-scroll-hint {
  position: absolute;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
}

.hero-scroll-hint span {
  display: block;
  width: 24px;
  height: 24px;
  border-right: 2px solid var(--text-muted);
  border-bottom: 2px solid var(--text-muted);
  transform: rotate(45deg);
  animation: scrollHint 2s ease-in-out infinite;
  opacity: 0.4;
}

@keyframes scrollHint {
  0%, 100% { transform: rotate(45deg) translate(0,0); opacity: 0.2; }
  50% { transform: rotate(45deg) translate(6px,6px); opacity: 0.6; }
}

/* ===================== 数据统计 ===================== */
.stats-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0;
  padding: 48px 24px;
  background: var(--bg-card, white);
  border-top: 1px solid var(--border-color, #eee);
  border-bottom: 1px solid var(--border-color, #eee);
}

.stat-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 0 60px;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-card:hover .stat-accent {
  width: 48px;
  background: var(--accent);
}

.stat-number {
  font-size: 42px;
  font-weight: 900;
  color: var(--text-primary);
  letter-spacing: -2px;
}

.stat-label {
  font-size: 13px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 2px;
}

.stat-accent {
  display: block;
  width: 24px;
  height: 3px;
  border-radius: 2px;
  background: var(--border-color);
  transition: width 0.3s, background 0.3s;
}

.stat-divider {
  width: 1px;
  height: 50px;
  background: var(--border-color, #e8e8e8);
}

/* ===================== 通用区块 ===================== */
.section {
  padding: 80px 0;
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 40px;
  padding: 0 48px;
}

.section-title {
  font-size: 36px;
  font-weight: 900;
  letter-spacing: -1.5px;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.section-subtitle {
  font-size: 15px;
  color: var(--text-muted);
  margin: 0;
}

.section-link {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--accent);
  text-decoration: none;
  font-size: 15px;
  font-weight: 700;
  transition: gap 0.2s;
}

.section-link:hover .link-arrow {
  transform: translateX(4px);
}

.link-arrow {
  transition: transform 0.2s;
  display: inline-block;
}

/* ===================== 游戏卡片 ===================== */
.games-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  padding: 0 48px;
}

.game-card {
  border-radius: 16px;
  overflow: hidden;
  background: var(--bg-card, white);
  border: 1px solid var(--border-color, #eee);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.game-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 24px 48px rgba(0,0,0,0.12);
}

.game-card-img {
  position: relative;
  aspect-ratio: 16/9;
  overflow: hidden;
}

.game-card-bg {
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

.game-card-overlay {
  position: absolute;
  inset: 0;
  z-index: 2;
  background: linear-gradient(to top, rgba(0,0,0,0.6), transparent 50%);
}

.game-card-body {
  padding: 20px;
  position: relative;
  z-index: 3;
  margin-top: -40px;
}

.game-card-cat {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 6px;
  background: var(--accent);
  color: white;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 10px;
}

.game-card-title {
  font-size: 20px;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.game-card-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 14px;
}

.game-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.game-card-dev {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 600;
}

/* ===================== 文章卡片 ===================== */
.articles-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  padding: 0 48px;
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
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
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

.article-card-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 4px 10px;
  border-radius: 6px;
  background: rgba(0,0,0,0.7);
  color: white;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.article-card-body {
  padding: 20px;
}

.article-card-game {
  display: inline-block;
  font-size: 12px;
  font-weight: 700;
  color: var(--accent);
  margin-bottom: 8px;
}

.article-card-title {
  font-size: 17px;
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
  font-size: 13px;
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
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-muted);
}

.meta-dot {
  opacity: 0.3;
}

/* ===================== 响应式 ===================== */
@media (max-width: 1024px) {
  .games-grid, .articles-grid {
    grid-template-columns: repeat(2, 1fr);
    padding: 0 24px;
  }
  .section-header {
    padding: 0 24px;
  }
}

@media (max-width: 768px) {
  .hero {
    min-height: 70vh;
    padding: 80px 20px 60px;
  }
  .hero h1 {
    font-size: 40px;
    letter-spacing: -1px;
  }
  .hero p {
    font-size: 16px;
  }
  .hero-actions {
    flex-direction: column;
    gap: 12px;
  }
  .btn-primary, .btn-secondary {
    width: 100%;
    text-align: center;
  }
  .stats-bar {
    flex-direction: column;
    gap: 24px;
    padding: 32px 24px;
  }
  .stat-divider {
    width: 60px;
    height: 1px;
  }
  .stat-card {
    padding: 0;
  }
  .games-grid, .articles-grid {
    grid-template-columns: 1fr;
    padding: 0 20px;
  }
  .section-header {
    padding: 0 20px;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  .section-title {
    font-size: 28px;
  }
}
</style>
