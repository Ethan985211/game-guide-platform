<template>
  <div class="article-detail page-container" v-if="article">
    <el-card>
      <!-- 文章头部 -->
      <div class="article-header">
        <h1>{{ article.title }}</h1>
        <div class="meta">
          <div class="author">
            <el-avatar :size="40">{{ article.author?.username?.[0] }}</el-avatar>
            <div>
              <div class="author-name">{{ article.author?.username }}</div>
              <div class="date">{{ formatDate(article.created_at) }}</div>
            </div>
          </div>
          <div class="stats">
            <span>👁️ {{ article.views }}</span>
            <span>❤️ {{ article.likes }}</span>
          </div>
        </div>
      </div>

      <!-- 文章内容 -->
      <div class="article-content" v-html="article.content"></div>

      <!-- 操作栏 -->
      <div class="actions">
        <el-button type="primary" @click="handleLike" :icon="Like">
          点赞 {{ article.likes }}
        </el-button>
        <el-button @click="$router.back()">返回</el-button>
      </div>
    </el-card>

    <!-- 评论区 -->
    <el-card class="comments-section">
      <template #header>
        <span>评论 ({{ comments.length }})</span>
      </template>

      <!-- 发布评论 -->
      <div class="comment-form" v-if="authStore.isLoggedIn">
        <el-input
          v-model="newComment"
          type="textarea"
          :rows="3"
          placeholder="写下你的评论..."
        />
        <el-button type="primary" @click="submitComment" style="margin-top: 12px">
          发布评论
        </el-button>
      </div>
      <el-empty v-else description="登录后参与评论" />

      <!-- 评论列表 -->
      <div class="comments-list">
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <div class="comment-header">
            <el-avatar :size="32">{{ comment.author?.username?.[0] }}</el-avatar>
            <div class="comment-info">
              <span class="comment-author">{{ comment.author?.username }}</span>
              <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
            </div>
            <el-button size="small" text @click="likeComment(comment.id)">
              ❤️ {{ comment.likes }}
            </el-button>
          </div>
          <div class="comment-content">{{ comment.content }}</div>
        </div>
      </div>
      <el-empty v-if="!comments.length" description="暂无评论" />
    </el-card>
  </div>

  <el-skeleton v-else-if="loading" />
  <el-empty v-else description="文章不存在" />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Like } from '@element-plus/icons-vue'
import { articleAPI, commentAPI } from '../api'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const authStore = useAuthStore()
const article = ref(null)
const comments = ref([])
const newComment = ref('')
const loading = ref(false)

const loadData = async () => {
  loading.value = true
  const articleId = route.params.id
  try {
    const [articleRes, commentsRes] = await Promise.all([
      articleAPI.getArticle(articleId),
      commentAPI.getComments(articleId)
    ])
    article.value = articleRes.data
    comments.value = commentsRes.data
  } catch (error) {
    console.error('加载失败', error)
  } finally {
    loading.value = false
  }
}

const handleLike = async () => {
  try {
    const response = await articleAPI.likeArticle(route.params.id)
    article.value.likes = response.data.likes
  } catch (error) {
    ElMessage.error('点赞失败')
  }
}

const submitComment = async () => {
  if (!newComment.value.trim()) return
  try {
    await commentAPI.createComment({
      article_id: parseInt(route.params.id),
      content: newComment.value
    })
    newComment.value = ''
    ElMessage.success('评论成功')
    loadData()
  } catch (error) {
    ElMessage.error('评论失败')
  }
}

const likeComment = async (id) => {
  try {
    await commentAPI.likeComment(id)
    loadData()
  } catch (error) {
    ElMessage.error('点赞失败')
  }
}

const formatDate = (date) => new Date(date).toLocaleDateString('zh-CN')

onMounted(loadData)
</script>

<style scoped>
.article-detail {
  padding-top: 20px;
}

.article-header {
  margin-bottom: 24px;
}

.article-header h1 {
  font-size: 28px;
  margin-bottom: 16px;
}

.meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.author {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-name {
  font-weight: 600;
}

.date {
  font-size: 13px;
  color: #909399;
}

.stats {
  display: flex;
  gap: 16px;
  color: #909399;
}

.article-content {
  line-height: 1.8;
  font-size: 16px;
  color: #303133;
  min-height: 200px;
}

.actions {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #ebeef5;
}

.comments-section {
  margin-top: 24px;
}

.comment-form {
  margin-bottom: 24px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-item {
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.comment-info {
  flex: 1;
}

.comment-author {
  font-weight: 600;
  margin-right: 8px;
}

.comment-date {
  font-size: 12px;
  color: #909399;
}

.comment-content {
  padding-left: 44px;
  line-height: 1.6;
  color: #606266;
}
</style>
