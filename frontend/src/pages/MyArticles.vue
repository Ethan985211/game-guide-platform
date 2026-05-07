<template>
  <div class="my-articles page-container">
    <h1 class="page-title">我的文章</h1>

    <div class="actions">
      <el-button type="primary" @click="$router.push('/articles/create')">发布新文章</el-button>
    </div>

    <div class="articles-list">
      <el-card v-for="article in articles" :key="article.id" class="article-item">
        <div class="article-content">
          <h3>{{ article.title }}</h3>
          <div class="meta">
            <el-tag size="small">{{ article.category }}</el-tag>
            <span>{{ formatDate(article.created_at) }}</span>
            <span>浏览 {{ article.views }}</span>
            <span>点赞 {{ article.likes }}</span>
          </div>
        </div>
        <div class="actions">
          <el-button size="small" @click="$router.push(`/articles/${article.id}`)">查看</el-button>
          <el-button size="small" type="danger" @click="deleteArticle(article.id)">删除</el-button>
        </div>
      </el-card>
    </div>

    <el-empty v-if="!articles.length" description="暂无文章" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
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
    articles.value = response.data
  } catch (error) {
    console.error('加载失败', error)
  }
}

const deleteArticle = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这篇文章吗？', '提示', {
      type: 'warning'
    })
    await articleAPI.deleteArticle(id)
    ElMessage.success('删除成功')
    loadArticles()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const formatDate = (date) => new Date(date).toLocaleDateString('zh-CN')

onMounted(loadArticles)
</script>

<style scoped>
.my-articles {
  padding-top: 20px;
}

.actions {
  margin-bottom: 20px;
}

.articles-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.article-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.article-content h3 {
  margin-bottom: 8px;
}

.meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #909399;
}
</style>
