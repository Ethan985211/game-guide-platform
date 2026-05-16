<template>
  <div class="game-detail" v-if="game">
    <!-- 英雄横幅 -->
    <div class="hero-banner">
      <div class="hero-bg" :style="{ backgroundImage: `url(${game.cover_image || ''})` }"></div>
      <div class="hero-gradient"></div>
      <div class="hero-content">
        <div class="hero-meta">
          <span class="hero-category">{{ game.category }}</span>
          <span class="hero-dot">·</span>
          <span>{{ game.developer }}</span>
        </div>
        <h1 class="hero-title">{{ game.name }}</h1>
        <p class="hero-desc">{{ game.description }}</p>
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-value">{{ game.views || 0 }}</span>
            <span class="stat-label">浏览</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ characters.length }}</span>
            <span class="stat-label">角色</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ articles.length }}</span>
            <span class="stat-label">攻略</span>
          </div>
        </div>
      </div>
    </div>

    <div class="page-body">
      <!-- 下载链接 -->
      <section class="section section-links" v-if="gameLinks.website || gameLinks.steam">
        <div class="section-header">
          <h2 class="section-title">游戏下载</h2>
        </div>
        <div class="links-row">
          <a v-if="gameLinks.website" :href="gameLinks.website" target="_blank" rel="noopener" class="link-btn link-official">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/></svg>
            官方网站
          </a>
          <a v-if="gameLinks.steam" :href="gameLinks.steam" target="_blank" rel="noopener" class="link-btn link-steam">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M11.974 0C5.362 0 0 5.362 0 11.974S5.362 23.948 11.974 23.948 23.948 18.586 23.948 11.974C23.948 5.362 18.586 0 11.974 0zm4.977 17.323l-1.793.76-1.628-2.362c-.39.155-.8.24-1.228.24a3.297 3.297 0 01-3.298-3.298 3.297 3.297 0 013.298-3.298 3.297 3.297 0 013.298 3.298c0 .484-.11.942-.296 1.358l1.347 1.956zm1.072-3.346l.61-1.753-3.608-2.637-.638 1.342 3.636 3.048z"/></svg>
            Steam 商店
          </a>
        </div>
      </section>

      <!-- 角色图鉴 -->
      <section class="section" v-if="characters.length">
        <div class="section-header">
          <h2 class="section-title">角色图鉴</h2>
          <span class="section-count">{{ characters.length }} 位角色</span>
        </div>
        <div class="characters-grid">
          <div v-for="char in characters" :key="char.id" class="character-card">
            <div class="char-visual">
              <div class="char-gradient" :class="rarityClass(char.rarity)"></div>
              <img
                :src="char.image || '/placeholder.png'"
                :alt="char.name"
                @error="onImgError"
                class="char-img"
              />
              <span class="char-rarity">{{ char.rarity || '' }}</span>
            </div>
            <div class="char-info">
              <h3 class="char-name">{{ char.name }}</h3>
              <div class="char-tags">
                <span v-if="char.element" class="tag tag-element">{{ char.element }}</span>
                <span v-if="char.weapon_type" class="tag tag-weapon">{{ char.weapon_type }}</span>
              </div>
              <p class="char-desc">{{ char.description?.slice(0, 60) }}{{ char.description?.length > 60 ? '...' : '' }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 相关攻略 -->
      <section class="section">
        <div class="section-header">
          <h2 class="section-title">相关攻略</h2>
          <span class="section-count">{{ articles.length }} 篇</span>
        </div>
        <div v-if="articles.length" class="articles-list">
          <div
            v-for="article in articles"
            :key="article.id"
            class="article-row"
            @click="goToArticle(article.id)"
          >
            <div class="article-row-img">
              <img
                :src="article.cover_image || game.cover_image || ''"
                :alt="article.title"
                @error="onImgError"
              />
            </div>
            <div class="article-row-content">
              <div class="article-row-header">
                <span class="article-category">{{ article.category === 'guide' ? '攻略' : article.category === 'tips' ? '心得' : '资讯' }}</span>
                <h3>{{ article.title }}</h3>
              </div>
              <div class="article-row-meta">
                <span>{{ article.views || 0 }} 阅读</span>
                <span class="meta-dot">·</span>
                <span>{{ article.likes || 0 }} 点赞</span>
                <span class="meta-dot">·</span>
                <span>{{ article.author?.username || '管理员' }}</span>
              </div>
            </div>
            <div class="article-row-arrow">→</div>
          </div>
        </div>
        <div v-else class="empty-hint">暂无相关攻略</div>
      </section>
    </div>
  </div>

  <div v-else-if="loading" class="loading-state">
    <div class="loading-spinner"></div>
    <p>加载中...</p>
  </div>
  <div v-else class="empty-state">
    <p>游戏不存在</p>
    <router-link to="/games">返回游戏库</router-link>
  </div>
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
const loading = ref(true)

const gameLinkMap = {
  1: { website: 'https://genshin.hoyoverse.com/', steam: '' },
  2: { website: 'https://www.honorofkings.com/', steam: '' },
  3: { website: 'https://hsr.hoyoverse.com/', steam: '' },
  4: { website: 'https://zenless.hoyoverse.com/', steam: 'https://store.steampowered.com/app/4162040/Zenless_Zone_Zero/' },
  5: { website: 'https://www.leagueoflegends.com/', steam: '' },
  6: { website: 'https://www.heishenhua.com/', steam: 'https://store.steampowered.com/app/2358720/Black_Myth_Wukong/' },
  7: { website: 'https://www.arknights.global/', steam: '' },
}

const gameLinks = computed(() => {
  if (!game.value) return {}
  return gameLinkMap[game.value.id] || {}
})

const rarityClass = (rarity) => {
  if (!rarity) return ''
  const r = rarity.toLowerCase()
  if (r.includes('五') || r.includes('5') || r.includes('ssr')) return 'rarity-legendary'
  if (r.includes('四') || r.includes('4') || r.includes('sr')) return 'rarity-epic'
  return ''
}

const onImgError = (e) => {
  e.target.style.display = 'none'
}

const goToArticle = (id) => router.push(`/articles/${id}`)

onMounted(async () => {
  const gameId = route.params.id
  try {
    const [gameRes, charRes, articleRes] = await Promise.all([
      gameAPI.getGame(gameId),
      gameAPI.getGameCharacters(gameId),
      articleAPI.getArticles({ game_id: gameId, limit: 10 })
    ])
    game.value = gameRes.data
    characters.value = charRes.data
    articles.value = articleRes.data?.items || articleRes.data || []
    analytics.recordContentView('game', gameId)
  } catch (err) {
    console.error('加载失败', err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
/* 英雄横幅 */
.hero-banner {
  position: relative;
  height: 480px;
  display: flex;
  align-items: flex-end;
  overflow: hidden;
  margin-bottom: 0;
}

.hero-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center 20%;
  background-repeat: no-repeat;
  filter: blur(0px);
  transform: scale(1.05);
}

.hero-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(0,0,0,0.2) 0%,
    rgba(0,0,0,0) 30%,
    rgba(0,0,0,0.6) 60%,
    rgba(0,0,0,0.95) 100%
  );
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 48px 60px;
  width: 100%;
}

.hero-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
  font-size: 14px;
  color: rgba(255,255,255,0.7);
  text-transform: uppercase;
  letter-spacing: 2px;
}

.hero-category {
  color: var(--accent);
  font-weight: 700;
}

.hero-dot {
  opacity: 0.4;
}

.hero-title {
  font-size: clamp(42px, 7vw, 72px);
  font-weight: 900;
  color: white;
  letter-spacing: -3px;
  line-height: 1;
  margin-bottom: 20px;
}

.hero-desc {
  font-size: 17px;
  color: rgba(255,255,255,0.8);
  line-height: 1.8;
  max-width: 650px;
  margin-bottom: 32px;
}

.hero-stats {
  display: flex;
  gap: 40px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-value {
  font-size: 32px;
  font-weight: 900;
  color: white;
  letter-spacing: -1px;
}

.stat-label {
  font-size: 12px;
  color: rgba(255,255,255,0.5);
  text-transform: uppercase;
  letter-spacing: 2px;
}

/* 页面主体 */
.page-body {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 48px 80px;
}

.section {
  padding: 64px 0;
  border-bottom: 1px solid var(--border-color, #e8e8e8);
}

.section:last-child {
  border-bottom: none;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 40px;
}

.section-title {
  font-size: 32px;
  font-weight: 900;
  letter-spacing: -1.5px;
  color: var(--text-primary);
  position: relative;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 0;
  width: 48px;
  height: 3px;
  background: var(--accent);
  border-radius: 2px;
}

.section-count {
  font-size: 14px;
  color: var(--text-muted);
}

/* 角色卡片网格 */
.characters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
}

.character-card {
  border-radius: 16px;
  overflow: hidden;
  background: var(--bg-card, white);
  border: 1px solid var(--border-color, #eee);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: default;
}

.character-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.12);
}

.char-visual {
  position: relative;
  aspect-ratio: 1;
  background: var(--bg-dark, #1a1a2e);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.char-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #2d2d44, #1a1a2e);
  z-index: 0;
}

.char-gradient.rarity-legendary {
  background: linear-gradient(135deg, #4a3a1a, #2a1a0a, #3a2a10);
}

.char-gradient.rarity-epic {
  background: linear-gradient(135deg, #3a1a3a, #1a0a2a, #2a103a);
}

.char-img {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.char-rarity {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 2;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  background: rgba(0,0,0,0.7);
  color: #ffd700;
  letter-spacing: 1px;
}

.char-info {
  padding: 20px;
}

.char-name {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.char-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}

.tag {
  padding: 3px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
}

.tag-element {
  background: #fff3e0;
  color: #e65100;
}

.tag-weapon {
  background: #e8eaf6;
  color: #283593;
}

.char-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
}

/* 文章列表 */
.articles-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.article-row {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px 24px;
  border-radius: 14px;
  background: var(--bg-card, white);
  border: 1px solid var(--border-color, #eee);
  cursor: pointer;
  transition: all 0.25s;
}

.article-row:hover {
  transform: translateX(6px);
  border-color: var(--accent);
  box-shadow: 0 4px 20px rgba(255,107,0,0.1);
}

.article-row-img {
  width: 100px;
  height: 70px;
  border-radius: 10px;
  overflow: hidden;
  flex-shrink: 0;
  background: var(--bg-dark);
}

.article-row-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-row-content {
  flex: 1;
  min-width: 0;
}

.article-row-header {
  margin-bottom: 8px;
}

.article-category {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  background: var(--accent-light, #fff3e0);
  color: var(--accent);
  margin-bottom: 6px;
}

.article-row h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.article-row-meta {
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  gap: 8px;
  align-items: center;
}

.meta-dot {
  opacity: 0.3;
}

.article-row-arrow {
  font-size: 20px;
  color: var(--text-muted);
  flex-shrink: 0;
  transition: transform 0.25s, color 0.25s;
}

.article-row:hover .article-row-arrow {
  transform: translateX(4px);
  color: var(--accent);
}

.empty-hint {
  text-align: center;
  color: var(--text-muted);
  padding: 40px;
  font-size: 15px;
}

/* 下载链接 */
.section-links {
  border-bottom: 1px solid var(--border-color, #e8e8e8);
}

.links-row {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.link-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.25s;
  border: 2px solid var(--border-color, #ddd);
  color: var(--text-primary);
  background: var(--bg-card, white);
}

.link-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(0,0,0,0.1);
}

.link-official:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.link-steam {
  background: #1a1a2e;
  border-color: #1a1a2e;
  color: #fff;
}

.link-steam:hover {
  background: #16213e;
  border-color: #16213e;
  color: #66c0f4;
}

/* 加载/空状态 */
.loading-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 16px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-color);
  border-top: 3px solid var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state a {
  color: var(--accent);
  font-weight: 600;
}

@media (max-width: 768px) {
  .hero-banner {
    height: 380px;
  }
  .hero-content {
    padding: 0 20px 40px;
  }
  .hero-title {
    font-size: 36px;
    letter-spacing: -1px;
  }
  .page-body {
    padding: 0 20px 60px;
  }
  .characters-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .article-row {
    flex-direction: column;
    align-items: flex-start;
  }
  .article-row-img {
    width: 100%;
    height: 140px;
  }
}
</style>
