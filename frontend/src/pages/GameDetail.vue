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
          <span class="hero-dot">·</span>
          <span v-if="game.release_date">{{ formatDate(game.release_date) }}</span>
        </div>
        <h1 class="hero-title">{{ game.name }}</h1>
        <p class="hero-desc">{{ game.description }}</p>
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-value">{{ articles.length }}</span>
            <span class="stat-label">攻略</span>
          </div>
          <div class="stat-item" v-if="characters.length">
            <span class="stat-value">{{ characters.length }}</span>
            <span class="stat-label">角色</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ game.views || 0 }}</span>
            <span class="stat-label">热度</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 快捷信息栏 -->
    <div class="info-bar" v-if="gameLinks.website || gameLinks.steam || game.publisher || game.release_date">
      <div class="info-bar-inner">
        <div class="info-meta">
          <div class="info-item" v-if="game.publisher">
            <span class="info-label">发行商</span>
            <span class="info-val">{{ game.publisher }}</span>
          </div>
          <div class="info-item" v-if="game.release_date">
            <span class="info-label">发售日</span>
            <span class="info-val">{{ formatDate(game.release_date) }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">开发商</span>
            <span class="info-val">{{ game.developer }}</span>
          </div>
        </div>
        <div class="info-actions" v-if="gameLinks.website || gameLinks.steam">
          <a v-if="gameLinks.website" :href="gameLinks.website" target="_blank" rel="noopener" class="action-link action-official">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/></svg>
            官网
          </a>
          <a v-if="gameLinks.steam" :href="gameLinks.steam" target="_blank" rel="noopener" class="action-link action-steam">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M11.974 0C5.362 0 0 5.362 0 11.974S5.362 23.948 11.974 23.948 23.948 18.586 23.948 11.974C23.948 5.362 18.586 0 11.974 0zm4.977 17.323l-1.793.76-1.628-2.362c-.39.155-.8.24-1.228.24a3.297 3.297 0 01-3.298-3.298 3.297 3.297 0 013.298-3.298 3.297 3.297 0 013.298 3.298c0 .484-.11.942-.296 1.358l1.347 1.956zm1.072-3.346l.61-1.753-3.608-2.637-.638 1.342 3.636 3.048z"/></svg>
            Steam
          </a>
        </div>
      </div>
    </div>

    <div class="page-body">
      <!-- 角色图鉴 -->
      <section class="section" v-if="characters.length">
        <div class="section-header">
          <h2 class="section-title">角色图鉴</h2>
          <span class="section-count">{{ characters.length }} 位</span>
        </div>
        <div class="characters-scroll">
          <div v-for="char in characters" :key="char.id" class="character-card">
            <div class="char-visual" :class="rarityClass(char.rarity)">
              <img
                :src="char.image || '/placeholder.png'"
                :alt="char.name"
                @error="onImgError"
                class="char-img"
              />
              <span class="char-rarity" v-if="char.rarity">{{ char.rarity }}</span>
            </div>
            <div class="char-info">
              <h3 class="char-name">{{ char.name }}</h3>
              <div class="char-tags">
                <span v-if="char.element" class="tag tag-element">{{ char.element }}</span>
                <span v-if="char.weapon_type" class="tag tag-weapon">{{ char.weapon_type }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 推广卡片 -->
      <section class="section">
        <PromoCard />
      </section>

      <!-- 相关攻略 -->
      <section class="section">
        <div class="section-header">
          <h2 class="section-title">相关攻略</h2>
          <span class="section-count">{{ articles.length }} 篇</span>
        </div>
        <div v-if="articles.length" class="articles-grid">
          <div
            v-for="article in articles"
            :key="article.id"
            class="article-card"
            @click="goToArticle(article.id)"
          >
            <div class="article-card-img">
              <img
                :src="article.cover_image || game.cover_image || ''"
                :alt="article.title"
                @error="onImgError"
              />
              <span class="article-card-badge">{{ categoryLabel(article.category) }}</span>
            </div>
            <div class="article-card-body">
              <h3 class="article-card-title">{{ article.title }}</h3>
              <p class="article-card-excerpt" v-if="article.content">
                {{ stripMarkdown(article.content).slice(0, 80) }}...
              </p>
              <div class="article-card-meta">
                <span>{{ article.views || 0 }} 阅读</span>
                <span class="meta-dot">·</span>
                <span>{{ article.likes || 0 }} 赞</span>
              </div>
            </div>
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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { gameAPI, articleAPI } from '../api'
import analytics from '../utils/analytics'
import PromoCard from '../components/PromoCard.vue'

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
  8: { website: 'https://wutheringwaves.kurogames.com/', steam: '' },
  9: { website: 'https://ht.wanmei.com/', steam: 'https://store.steampowered.com/app/2064650/Tower_of_Fantasy/' },
  10: { website: 'https://bh3.mihoyo.com/', steam: 'https://store.steampowered.com/app/2501360/Honkai_Impact_3rd/' },
  11: { website: 'https://www.yjwujian.cn/', steam: 'https://store.steampowered.com/app/1203220/NARAKA_BLADEPOINT/' },
  12: { website: 'https://df.qq.com/', steam: '' },
  13: { website: 'https://mdnf.qq.com/', steam: '' },
  14: { website: 'https://blhx.biligame.com/', steam: '' },
  15: { website: 'https://gf2.sunborngame.com/', steam: '' },
  16: { website: 'https://www.eldenring.jp/', steam: 'https://store.steampowered.com/app/1245620/ELDEN_RING/' },
  17: { website: 'https://www.cyberpunk.net/', steam: 'https://store.steampowered.com/app/1091500/Cyberpunk_2077/' },
  18: { website: 'https://www.zelda.com/tears-of-the-kingdom/', steam: '' },
  19: { website: 'https://www.jp.square-enix.com/ffvii_rebirth/', steam: 'https://store.steampowered.com/app/2909400/FINAL_FANTASY_VII_REBIRTH/' },
  20: { website: 'https://www.rockstargames.com/VI', steam: '' },
  21: { website: 'https://www.monsterhunter.com/wilds/', steam: 'https://store.steampowered.com/app/2246340/Monster_Hunter_Wilds/' },
  22: { website: 'https://www.kojimaproductions.jp/death-stranding-2', steam: '' },
  23: { website: 'https://civilization.2k.com/civ-vii/', steam: 'https://store.steampowered.com/app/289070/Sid_Meiers_Civilization_VII/' },
  24: { website: 'https://raft-game.com/', steam: 'https://store.steampowered.com/app/648800/Raft/' },
}

const gameLinks = computed(() => {
  if (!game.value) return {}
  return gameLinkMap[game.value.id] || {}
})

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  try {
    const d = new Date(dateStr)
    return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`
  } catch { return dateStr }
}

const stripMarkdown = (text) => {
  if (!text) return ''
  return text.replace(/[#*`>\[\]|\\-]/g, '').replace(/\n+/g, ' ').trim()
}

const categoryLabel = (cat) => {
  const map = { guide: '攻略', tips: '心得', news: '资讯' }
  return map[cat] || cat || '攻略'
}

const rarityClass = (rarity) => {
  if (!rarity) return ''
  const r = rarity.toLowerCase()
  if (r.includes('五') || r.includes('5') || r.includes('ssr')) return 'char-legendary'
  if (r.includes('四') || r.includes('4') || r.includes('sr')) return 'char-epic'
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
/* ============ 英雄横幅 ============ */
.hero-banner {
  position: relative;
  height: 420px;
  display: flex;
  align-items: flex-end;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center 25%;
  background-repeat: no-repeat;
  transform: scale(1.03);
}

.hero-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(0,0,0,0.15) 0%,
    rgba(0,0,0,0) 25%,
    rgba(0,0,0,0.5) 55%,
    rgba(0,0,0,0.92) 100%
  );
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 48px 48px;
  width: 100%;
}

.hero-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
  font-size: 13px;
  color: rgba(255,255,255,0.65);
  text-transform: uppercase;
  letter-spacing: 1.5px;
}

.hero-category {
  color: var(--accent);
  font-weight: 700;
}

.hero-dot {
  opacity: 0.35;
}

.hero-title {
  font-size: clamp(44px, 8vw, 80px);
  font-weight: 900;
  color: white;
  letter-spacing: -3px;
  line-height: 0.95;
  margin-bottom: 16px;
}

.hero-desc {
  font-size: 16px;
  color: rgba(255,255,255,0.75);
  line-height: 1.8;
  max-width: 580px;
  margin-bottom: 28px;
}

.hero-stats {
  display: flex;
  gap: 40px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.stat-value {
  font-size: 28px;
  font-weight: 900;
  color: white;
  letter-spacing: -1px;
}

.stat-label {
  font-size: 11px;
  color: rgba(255,255,255,0.45);
  text-transform: uppercase;
  letter-spacing: 2px;
}

/* ============ 快捷信息栏 ============ */
.info-bar {
  background: var(--bg-card, rgba(255,255,255,0.04));
  border-bottom: 1px solid var(--border-color, rgba(255,255,255,0.08));
  backdrop-filter: blur(20px);
  position: sticky;
  top: 0;
  z-index: 10;
}

.info-bar-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 48px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 56px;
  gap: 24px;
}

.info-meta {
  display: flex;
  gap: 28px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.info-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--text-muted, #999);
}

.info-val {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.info-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.action-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 18px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.2s;
}

.action-official {
  background: var(--accent);
  color: white;
}

.action-official:hover {
  filter: brightness(1.15);
  transform: translateY(-1px);
}

.action-steam {
  background: #1a1a2e;
  color: #c4d6ff;
  border: 1px solid rgba(255,255,255,0.1);
}

.action-steam:hover {
  background: #232340;
  color: #66c0f4;
  transform: translateY(-1px);
}

/* ============ 页面主体 ============ */
.page-body {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 48px 80px;
}

.section {
  padding: 56px 0;
  border-bottom: 1px solid var(--border-color, rgba(0,0,0,0.06));
}

.section:last-child {
  border-bottom: none;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 36px;
}

.section-title {
  font-size: 28px;
  font-weight: 900;
  letter-spacing: -1px;
  color: var(--text-primary);
  position: relative;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 40px;
  height: 3px;
  background: var(--accent);
  border-radius: 2px;
}

.section-count {
  font-size: 13px;
  color: var(--text-muted);
}

/* ============ 角色卡片：紧凑横向滚动 ============ */
.characters-scroll {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 16px;
}

.character-card {
  border-radius: 14px;
  overflow: hidden;
  background: var(--bg-card, white);
  border: 1px solid var(--border-color, #eee);
  transition: transform 0.25s, box-shadow 0.25s;
  cursor: default;
}

.character-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.1);
}

.char-visual {
  position: relative;
  aspect-ratio: 1;
  background: #1a1a2e;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.char-visual.char-legendary {
  background: linear-gradient(135deg, #3a2a0a, #1a0a00);
}

.char-visual.char-epic {
  background: linear-gradient(135deg, #2a1a3a, #0a0a1a);
}

.char-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.char-rarity {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 700;
  background: rgba(0,0,0,0.7);
  color: #ffd700;
  letter-spacing: 0.5px;
}

.char-info {
  padding: 12px 14px;
}

.char-name {
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 6px;
  color: var(--text-primary);
}

.char-tags {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.tag {
  padding: 2px 7px;
  border-radius: 4px;
  font-size: 10px;
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

/* ============ 攻略文章卡片网格 ============ */
.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
  gap: 20px;
}

.article-card {
  border-radius: 14px;
  overflow: hidden;
  background: var(--bg-card, white);
  border: 1px solid var(--border-color, #eee);
  cursor: pointer;
  transition: all 0.25s;
  display: flex;
  flex-direction: column;
}

.article-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0,0,0,0.1);
  border-color: var(--accent);
}

.article-card-img {
  position: relative;
  aspect-ratio: 16/9;
  overflow: hidden;
  background: var(--bg-dark, #1a1a2e);
}

.article-card-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s;
}

.article-card:hover .article-card-img img {
  transform: scale(1.06);
}

.article-card-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  background: rgba(0,0,0,0.65);
  color: var(--accent);
  backdrop-filter: blur(4px);
}

.article-card-body {
  padding: 18px 20px 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.article-card-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.4;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-card-excerpt {
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.6;
  margin-bottom: 12px;
  flex: 1;
}

.article-card-meta {
  display: flex;
  gap: 8px;
  align-items: center;
  font-size: 12px;
  color: var(--text-muted);
}

.meta-dot {
  opacity: 0.3;
}

/* ============ 通用状态 ============ */
.empty-hint {
  text-align: center;
  color: var(--text-muted);
  padding: 48px;
  font-size: 15px;
}

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

/* ============ 响应式 ============ */
@media (max-width: 768px) {
  .hero-banner {
    height: 340px;
  }
  .hero-content {
    padding: 0 20px 36px;
  }
  .hero-title {
    font-size: 34px;
    letter-spacing: -1px;
  }
  .hero-desc {
    font-size: 14px;
    max-width: 100%;
  }
  .page-body {
    padding: 0 20px 60px;
  }
  .info-bar-inner {
    padding: 0 20px;
    flex-direction: column;
    height: auto;
    padding-top: 14px;
    padding-bottom: 14px;
    gap: 12px;
  }
  .info-meta {
    gap: 18px;
    flex-wrap: wrap;
  }
  .characters-scroll {
    grid-template-columns: repeat(3, 1fr);
  }
  .articles-grid {
    grid-template-columns: 1fr;
  }
}
</style>
