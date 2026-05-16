<template>
  <div class="my-articles page">
    <div class="page-header">
      <h1 class="page-title">我的文章</h1>
      <p class="page-subtitle">管理你发布的游戏攻略和资讯</p>
    </div>

    <div class="actions-bar">
      <div class="articles-count">
        共 <span class="count">{{ articles.length }}</span> 篇文章
      </div>
      <el-button type="primary" size="large" @click="$router.push('/articles/create')">
        <el-icon><Plus /></el-icon>
        发布新文章
      </el-button>
    </div>

    <div class="articles-list" v-if="articles.length">
      <div 
        v-for="article in articles" 
        :key="article.id" 
        class="article-card"
      >
        <div class="article-image" v-if="article.cover_image">
          <img :src="article.cover_image" :alt="article.title" />
        </div>
        <div class="article-image placeholder" v-else>
          <el-icon><Document /></el-icon>
        </div>
        
        <div class="article-body">
          <div class="article-header">
            <el-tag size="small" type="warning" effect="dark">{{ article.category }}</el-tag>
            <span class="article-date">{{ formatDate(article.created_at) }}</span>
          </div>
          
          <h3 class="article-title">{{ article.title }}</h3>
          
          <p class="article-excerpt" v-if="article.content">
            {{ stripHtml(article.content).slice(0, 100) }}...
          </p>
          
          <div class="article-stats">
            <span class="stat">
              <el-icon><View /></el-icon>
              {{ article.views }} 浏览
            </span>
            <span class="stat">
              <el-icon><Star /></el-icon>
              {{ article.likes }} 点赞
            </span>
            <span class="stat">
              <el-icon><ChatDotRound /></el-icon>
              {{ article.comments || 0 }} 评论
            </span>
          </div>
        </div>
        
        <div class="article-actions">
          <el-button type="primary" plain @click="$router.push(`/articles/${article.id}`)">
            <el-icon><View /></el-icon>
            查看
          </el-button>
          <el-button type="warning" plain @click="$router.push(`/articles/${article.id}/edit`)">
            <el-icon><Edit /></el-icon>
            编辑
          </el-button>
          <el-button type="danger" plain @click="deleteArticle(article.id)">
            <el-icon><Delete /></el-icon>
            删除
          </el-button>
        </div>
      </div>
    </div>

    <el-empty v-else description="还没有发布过文章" class="empty-state">
      <el-button type="primary" @click="$router.push('/articles/create')">
        立即发布
      </el-button>
    </el-empty>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Document, View, Star, ChatDotRound, Edit, Delete } from '@element-plus/icons-vue'
import { articleAPI } from '../api'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const articles = ref([])

const loadArticles = async () => {
  try {
    const response = await articleAPI.getArticles({
      author_id: authStore.user?.id,
      limit: 100
    })
    articles.value = response.data || []
  } catch (error) {
    console.error('加载失败', error)
    ElMessage.error('加载文章列表失败')
  }
}

const deleteArticle = async (id) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这篇文章吗？删除后无法恢复。', 
      '删除确认', 
      {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )
    await articleAPI.deleteArticle(id)
    ElMessage.success('删除成功')
    loadArticles()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const stripHtml = (html) => {
  if (!html) return ''
  return html.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ')
}

onMounted(loadArticles)
</script>

<style scoped>
.my-articles {
  max-width: 1000px;
  margin: 0 auto;
  padding: 80px 48px;
}

.page-header {
  margin-bottom: 40px;
}

.page-title {
  font-size: 48px;
  font-weight: 900;
  letter-spacing: -2px;
  margin-bottom: 12px;
  position: relative;
  display: inline-block;
  color: var(--text-primary);
}

.page-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 80px;
  height: 4px;
  background: var(--accent);
  border-radius: 2px;
}

.page-subtitle {
  font-size: 16px;
  color: var(--text-secondary);
  margin-top: 24px;
}

/* 操作栏 */
.actions-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding: 20px 24px;
  background: var(--bg-secondary);
  border-radius: 12px;
}

.articles-count {
  font-size: 15px;
  color: var(--text-secondary);
}

.articles-count .count {
  font-weight: 800;
  color: var(--accent);
  font-size: 18px;
}

.actions-bar :deep(.el-button--primary) {
  background: var(--accent);
  border-color: var(--accent);
  font-weight: 700;
  border-radius: 8px;
}

.actions-bar :deep(.el-button--primary:hover) {
  background: var(--accent-hover);
  border-color: var(--accent-hover);
}

/* 文章列表 */
.articles-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.article-card {
  display: flex;
  gap: 24px;
  background: white;
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s ease;
  position: relative;
}

.article-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 0;
  background: var(--accent);
  border-radius: 4px 0 0 4px;
  transition: height 0.3s ease;
}

.article-card:hover {
  border-color: var(--accent);
  box-shadow: 0 8px 24px rgba(255, 107, 0, 0.12);
  transform: translateY(-2px);
}

.article-card:hover::before {
  height: 100%;
}

/* 文章图片 */
.article-image {
  width: 160px;
  height: 120px;
  border-radius: 10px;
  overflow: hidden;
  flex-shrink: 0;
}

.article-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.article-card:hover .article-image img {
  transform: scale(1.05);
}

.article-image.placeholder {
  background: linear-gradient(135deg, var(--bg-secondary) 0%, #e8e8e8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  font-size: 40px;
}

/* 文章内容 */
.article-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.article-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.article-date {
  font-size: 13px;
  color: var(--text-muted);
}

.article-title {
  font-size: 20px;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 10px;
  line-height: 1.3;
  letter-spacing: -0.5px;
  transition: color 0.2s;
}

.article-card:hover .article-title {
  color: var(--accent);
}

.article-excerpt {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 12px;
  flex: 1;
}

.article-stats {
  display: flex;
  gap: 20px;
}

.stat {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--text-muted);
}

.stat .el-icon {
  font-size: 14px;
}

/* 操作按钮 */
.article-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  justify-content: center;
}

.article-actions :deep(.el-button) {
  border-radius: 8px;
  font-weight: 600;
}

/* 空状态 */
.empty-state {
  padding: 80px 0;
}

.empty-state :deep(.el-button--primary) {
  background: var(--accent);
  border-color: var(--accent);
  font-weight: 700;
}

.empty-state :deep(.el-button--primary:hover) {
  background: var(--accent-hover);
  border-color: var(--accent-hover);
}

/* 响应式 */
@media (max-width: 768px) {
  .my-articles {
    padding: 60px 20px;
  }
  
  .page-title {
    font-size: 36px;
  }
  
  .article-card {
    flex-direction: column;
  }
  
  .article-image {
    width: 100%;
    height: 160px;
  }
  
  .article-actions {
    flex-direction: row;
    justify-content: flex-start;
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid var(--border);
  }
  
  .actions-bar {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
}
</style>
