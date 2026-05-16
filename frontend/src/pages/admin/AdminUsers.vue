<template>
  <div class="admin-page">
    <aside class="admin-sidebar">
      <div class="sidebar-header">
        <h2>管理后台</h2>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/admin" exact-active-class="active">
          <el-icon><DataAnalysis /></el-icon>
          仪表盘
        </router-link>
        <router-link to="/admin/users" active-class="active">
          <el-icon><UserFilled /></el-icon>
          用户管理
        </router-link>
        <router-link to="/admin/games" active-class="active">
          <el-icon><Operation /></el-icon>
          游戏管理
        </router-link>
        <router-link to="/admin/characters" active-class="active">
          <el-icon><Avatar /></el-icon>
          角色管理
        </router-link>
        <router-link to="/admin/articles" active-class="active">
          <el-icon><Document /></el-icon>
          文章管理
        </router-link>
        <router-link to="/admin/hermes" active-class="active">
          <el-icon><Connection /></el-icon>
          Hermes Agent
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <button @click="handleLogout" class="logout-btn">
          <el-icon><SwitchButton /></el-icon>
          退出登录
        </button>
      </div>
    </aside>

    <main class="admin-main">
      <div class="admin-content">
        <div class="page-header">
          <h1 class="page-title">数据统计</h1>
          <div class="time-selector">
            <el-radio-group v-model="timeRange" size="default" @change="handleTimeRangeChange">
              <el-radio-button value="7">近7天</el-radio-button>
              <el-radio-button value="30">近30天</el-radio-button>
              <el-radio-button value="90">近90天</el-radio-button>
            </el-radio-group>
          </div>
        </div>

        <!-- 核心指标卡片 -->
        <div class="stats-grid">
          <div class="stat-card highlight">
            <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
              <el-icon><View /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ formatNumber(stats.totalViews) }}</span>
              <span class="stat-label">总浏览量</span>
              <span class="stat-trend up" v-if="stats.viewGrowth > 0">
                <el-icon><Top /></el-icon>
                +{{ stats.viewGrowth }}%
              </span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%)">
              <el-icon><TrendCharts /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ formatNumber(stats.todayViews) }}</span>
              <span class="stat-label">今日浏览</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)">
              <el-icon><Document /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ stats.totalArticles }}</span>
              <span class="stat-label">发布文章</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)">
              <el-icon><Monitor /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ stats.totalGames }}</span>
              <span class="stat-label">收录游戏</span>
            </div>
          </div>
        </div>

        <!-- 图表区域 -->
        <div class="charts-grid">
          <!-- 访问趋势图 -->
          <div class="chart-card">
            <h3>访问趋势</h3>
            <div class="bar-chart">
              <div v-for="item in trendData" :key="item.date" class="bar-item">
                <div class="bar-label">{{ item.date.split('-').slice(1).join('/') }}</div>
                <div class="bar-wrapper">
                  <div class="bar" :style="{ width: getBarWidth(item.views) + '%' }"></div>
                </div>
                <div class="bar-value">{{ formatNumber(item.views) }}</div>
              </div>
            </div>
          </div>

          <!-- 文章分类分布 -->
          <div class="chart-card">
            <h3>文章分类分布</h3>
            <div class="category-list">
              <div class="category-item" v-for="cat in categoryData" :key="cat.name">
                <span class="category-dot" :style="{ background: cat.color }"></span>
                <span class="category-name">{{ cat.name }}</span>
                <span class="category-value">{{ cat.value }}%</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 热门内容排行 -->
        <div class="rankings-section">
          <h2>热门内容排行</h2>
          <div class="rankings-grid">
            <!-- 游戏浏览排行 -->
            <div class="ranking-card">
              <h4><el-icon><Monitor /></el-icon> 游戏浏览排行</h4>
              <div class="ranking-list" v-loading="loadingGames">
                <div 
                  v-for="(game, index) in topGames" 
                  :key="game.id"
                  class="ranking-item"
                >
                  <span class="rank-number" :class="getRankClass(index)">{{ index + 1 }}</span>
                  <router-link :to="`/games/${game.slug}`" class="rank-name">{{ game.name }}</router-link>
                  <span class="rank-value">{{ formatNumber(game.views) }} 浏览</span>
                </div>
                <div v-if="topGames.length === 0 && !loadingGames" class="empty-tip">
                  暂无游戏数据
                </div>
              </div>
            </div>

            <!-- 文章浏览排行 -->
            <div class="ranking-card">
              <h4><el-icon><Document /></el-icon> 文章浏览排行</h4>
              <div class="ranking-list" v-loading="loadingArticles">
                <div 
                  v-for="(article, index) in topArticles" 
                  :key="article.id"
                  class="ranking-item"
                >
                  <span class="rank-number" :class="getRankClass(index)">{{ index + 1 }}</span>
                  <router-link :to="`/articles/${article.slug}`" class="rank-name">{{ article.title }}</router-link>
                  <span class="rank-value">{{ formatNumber(article.views) }} 浏览</span>
                </div>
                <div v-if="topArticles.length === 0 && !loadingArticles" class="empty-tip">
                  暂无文章数据
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 近期数据 -->
        <div class="recent-section">
          <h2>近期数据（7天）</h2>
          <div class="recent-grid">
            <div class="recent-card">
              <span class="recent-value">{{ formatNumber(stats.recentViews) }}</span>
              <span class="recent-label">新增浏览</span>
            </div>
            <div class="recent-card">
              <span class="recent-value">{{ stats.recentArticles }}</span>
              <span class="recent-label">新增文章</span>
            </div>
            <div class="recent-card">
              <span class="recent-value">{{ stats.totalGames }}</span>
              <span class="recent-label">收录游戏</span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAdminStore } from '../../stores/admin'
import {
  DataAnalysis, UserFilled, Document, Monitor, Connection,
  SwitchButton, View, TrendCharts, Top, Bottom, Operation,
  Avatar, ChatDotRound
} from '@element-plus/icons-vue'

const router = useRouter()
const adminStore = useAdminStore()

const timeRange = ref('7')
const loadingGames = ref(false)
const loadingArticles = ref(false)

// 趋势数据
const trendData = ref([])
const maxViews = ref(1)

// 分类数据（从后端获取真实数据）
const categoryData = ref([])

// 统计数据
const stats = reactive({
  totalViews: 0,
  todayViews: 0,
  viewGrowth: 0,
  totalArticles: 0,
  totalGames: 0,
  recentViews: 0
})

// 排行榜数据
const topGames = ref([])
const topArticles = ref([])

const formatNumber = (num) => {
  if (!num) return '0'
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  }
  return num?.toLocaleString() || '0'
}

const getRankClass = (index) => {
  if (index === 0) return 'gold'
  if (index === 1) return 'silver'
  if (index === 2) return 'bronze'
  return ''
}

// 获取统计数据
const fetchStats = async () => {
  try {
    const data = await adminStore.fetchStats()
    stats.totalViews = data.total_views || 0
    stats.todayViews = data.today_views || 0
    stats.totalArticles = data.total_articles || 0
    stats.totalGames = data.total_games || 0
    stats.recentViews = data.recent_views || 0
    
    // 计算增长趋势
    if (stats.recentViews > 0) {
      stats.viewGrowth = Math.round((stats.recentViews / stats.totalViews) * 100)
    }
  } catch (err) {
    console.error('获取统计数据失败:', err)
  }
}

// 获取游戏排行榜
const fetchTopGames = async () => {
  loadingGames.value = true
  try {
    topGames.value = await adminStore.fetchTopGames(5)
  } catch (err) {
    console.error('获取游戏排行失败:', err)
  } finally {
    loadingGames.value = false
  }
}

// 获取文章排行榜
const fetchTopArticles = async () => {
  loadingArticles.value = true
  try {
    topArticles.value = await adminStore.fetchTopArticles(5)
  } catch (err) {
    console.error('获取文章排行失败:', err)
  } finally {
    loadingArticles.value = false
  }
}

// 获取趋势数据
const fetchTrendData = async () => {
  try {
    const data = await adminStore.fetchViewsTrend(parseInt(timeRange.value))
    trendData.value = data || []
    maxViews.value = Math.max(...(data?.map(d => d.views) || [1]), 1)
  } catch (err) {
    console.error('获取趋势数据失败:', err)
    trendData.value = []
  }
}

// 获取文章分类统计（真实数据）
const fetchCategoryData = async () => {
  try {
    const data = await adminStore.fetchArticleCategories()
    categoryData.value = data || []
  } catch (err) {
    console.error('获取分类数据失败:', err)
    categoryData.value = []
  }
}

// 计算条形图宽度百分比
const getBarWidth = (views) => {
  return Math.round((views / maxViews.value) * 100)
}

const handleTimeRangeChange = () => {
  fetchTrendData()
}

onMounted(async () => {
  if (!adminStore.isLoggedIn) {
    router.push('/admin/login')
    return
  }
  
  // 并行加载所有数据
  await Promise.all([
    fetchStats(),
    fetchTopGames(),
    fetchTopArticles(),
    fetchTrendData(),
    fetchCategoryData()
  ])
})

const handleLogout = () => {
  adminStore.logout()
  ElMessage.success('已退出登录')
  router.push('/admin/login')
}
</script>

<style scoped>
.admin-page {
  display: flex;
  min-height: 100vh;
  background: #f5f7fa;
}

.admin-sidebar {
  width: 240px;
  background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
  color: white;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header h2 {
  font-size: 18px;
  font-weight: 700;
  color: #ff8c00;
}

.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
}

.sidebar-nav a {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  border-radius: 10px;
  margin-bottom: 4px;
  transition: all 0.3s;
  font-size: 14px;
}

.sidebar-nav a:hover,
.sidebar-nav a.active {
  background: rgba(255, 140, 0, 0.2);
  color: #ff8c00;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.3s;
}

.logout-btn:hover {
  background: rgba(255, 100, 100, 0.3);
  color: #ff6b6b;
}

.admin-main {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.admin-content {
  max-width: 1400px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s, box-shadow 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.stat-card.highlight {
  border: 2px solid #667eea;
  background: linear-gradient(135deg, #f8f9ff 0%, #fff 100%);
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: white;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #1a1a1a;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-top: 4px;
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  margin-top: 4px;
}

.stat-trend.up {
  color: #67c23a;
}

/* 图表区域 */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  margin-bottom: 24px;
}

.chart-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.chart-card h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 20px;
}

.chart-container {
  width: 100%;
  height: 300px;
}

/* 条形图样式 */
.bar-chart {
  padding: 10px 0;
}

.bar-item {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.bar-label {
  width: 60px;
  font-size: 13px;
  color: #666;
  text-align: right;
  padding-right: 12px;
}

.bar-wrapper {
  flex: 1;
  height: 24px;
  background: #f0f2f5;
  border-radius: 4px;
  overflow: hidden;
  margin: 0 12px;
}

.bar {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 4px;
  transition: width 0.5s ease;
  min-width: 4px;
}

.bar-value {
  width: 60px;
  font-size: 13px;
  color: #333;
  font-weight: 600;
}

/* 分类列表样式 */
.category-list {
  padding: 10px 0;
}

.category-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.category-item:last-child {
  border-bottom: none;
}

.category-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 12px;
}

.category-name {
  flex: 1;
  font-size: 14px;
  color: #333;
}

.category-value {
  font-size: 14px;
  font-weight: 600;
  color: #667eea;
}

/* 排行区域 */
.rankings-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.rankings-section h2 {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 20px;
}

.rankings-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.ranking-card {
  border: 1px solid #f0f0f0;
  border-radius: 10px;
  padding: 20px;
}

.ranking-card h4 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
}

.ranking-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ranking-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  background: #f8f9fa;
  border-radius: 8px;
  transition: background 0.2s;
}

.ranking-item:hover {
  background: #f0f2f5;
}

.rank-number {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 700;
  background: #e4e7ed;
  color: #666;
}

.rank-number.gold {
  background: linear-gradient(135deg, #ffd700, #ffb800);
  color: #fff;
}

.rank-number.silver {
  background: linear-gradient(135deg, #c0c0c0, #a8a8a8);
  color: #fff;
}

.rank-number.bronze {
  background: linear-gradient(135deg, #cd7f32, #b87333);
  color: #fff;
}

.rank-name {
  flex: 1;
  font-size: 14px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-decoration: none;
}

.rank-name:hover {
  color: #ff8c00;
}

.rank-value {
  font-size: 13px;
  color: #999;
}

.empty-tip {
  text-align: center;
  color: #999;
  padding: 20px;
  font-size: 14px;
}

/* 近期数据 */
.recent-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.recent-section h2 {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 20px;
}

.recent-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.recent-card {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
}

.recent-value {
  display: block;
  font-size: 36px;
  font-weight: 700;
  color: #ff8c00;
}

.recent-label {
  display: block;
  font-size: 14px;
  color: #666;
  margin-top: 8px;
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .charts-grid,
  .rankings-grid,
  .recent-grid {
    grid-template-columns: 1fr;
  }
}
</style>
