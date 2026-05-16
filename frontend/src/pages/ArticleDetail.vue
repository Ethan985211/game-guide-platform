<template>
  <div class="article-detail page-container" v-if="article">
    <el-card class="article-card-main">
      <div class="article-header">
        <h1>{{ article.title }}</h1>
        <div class="meta">
          <div class="author">
            <el-avatar :size="48" style="background: var(--gradient-primary)">
              {{ article.author?.username?.[0] }}
            </el-avatar>
            <div>
              <div class="author-name">{{ article.author?.username }}</div>
              <div class="date">{{ formatDate(article.created_at) }}</div>
            </div>
          </div>
          <div class="stats">
            <span>{{ article.views }} 阅读</span>
            <span>{{ article.likes }} 点赞</span>
          </div>
        </div>
      </div>

      <div class="article-content" v-html="article.content"></div>

      <div class="actions">
        <el-button type="primary" size="large" @click="handleLike" :icon="Star">
          点赞 {{ article.likes }}
        </el-button>
        <el-button size="large" @click="$router.back()">返回</el-button>
      </div>
    </el-card>


  </div>

  <el-skeleton v-else-if="loading" animated />
  <el-empty v-else description="文章不存在" />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Star } from '@element-plus/icons-vue'
import { articleAPI } from '../api'

const route = useRoute()
const article = ref(null)
const loading = ref(false)

const loadData = async () => {
  loading.value = true
  const articleId = route.params.id
  try {
    const articleRes = await articleAPI.getArticle(articleId)
    article.value = articleRes.data
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

const formatDate = (date) => new Date(date).toLocaleDateString('zh-CN')

onMounted(loadData)
</script>

<style scoped>
.article-card-main {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 20px;
}

.article-header {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--border-color);
}

.article-header h1 {
  font-size: 32px;
  margin-bottom: 20px;
  line-height: 1.3;
}

.meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.author {
  display: flex;
  align-items: center;
  gap: 14px;
}

.author-name {
  font-weight: 600;
  font-size: 16px;
}

.date {
  font-size: 13px;
  color: var(--text-muted);
}

.stats {
  display: flex;
  gap: 20px;
  font-size: 15px;
  color: var(--text-muted);
}

.article-content {
  line-height: 1.9;
  font-size: 16px;
  color: var(--text-secondary);
  min-height: 200px;
}

.actions {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--border-color);
}
</style>
