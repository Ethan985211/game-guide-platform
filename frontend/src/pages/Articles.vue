<template>
  <div class="articles page-container">
    <h1 class="page-title">攻略文章</h1>

    <!-- 筛选 -->
    <div class="filters">
      <el-input
        v-model="searchQuery"
        placeholder="搜索文章..."
        clearable
        style="width: 300px"
        @change="loadArticles"
      />
      <el-select v-model="category" placeholder="文章类型" clearable @change="loadArticles">
        <el-option label="攻略" value="guide" />
        <el-option label="资讯" value="news" />
        <el-option label="技巧" value="tips" />
      </el-select>
      <el-button type="primary" @click="$router.push('/articles/create')">发布文章</el-button>
    </div>

    <!-- 文章列表 -->
    <div class="articles-list">
      <div v-for="article in articles" :key="article.id" class="article-card" @click="goToArticle(article.id)">
        <div class="article-content">
          <h3>{{ article.title }}</h3>
          <p class="article-excerpt">{{ article.content.substring(0, 150) }}...</p>
        </div>
        <div class="article-footer">
          <div class="author">
            <el-avatar :size="24">{{ article.author?.username?.[0] }}</el-avatar>
            <span>{{ article.author?.username }}</span>
          </div>
          <div class="stats">
            <span>👁️ {{ article.views }}</span>
            <span>❤️ {{ article.likes }}</span>
            <span>{{ formatDate(article.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="20"
        :total="total"
        layout="prev, pager, next"
        @current-change="loadArticles"
      />
    </div>

    <el-empty v-if="!articles.length && !loading" description="暂无文章" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { articleAPI } from '../api'

const router = useRouter()
const articles = ref([])
const searchQuery = ref('')
const category = ref('')
const currentPage = ref(1)
const total = ref(0)
const loading = ref(false)

const loadArticles = async () => {
  loading.value = true
  try {
    const response = await articleAPI.getArticles({
      search: searchQuery.value,
      category: category.value,
      skip: (currentPage.value - 1) * 20,
      limit: 20
    })
    articles.value = response.data
    total.value = response.data.length
  } catch (error) {
    console.error('加载文章失败', error)
  } finally {
    loading.value = false
  }
}

const goToArticle = (id) => router.push(`/articles/${id}`)
const formatDate = (date) => new Date(date).toLocaleDateString('zh-CN')

onMounted(loadArticles)
</script>

<style scoped>
.articles {
  padding-top: 20px;
}

.filters {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.articles-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.article-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: transform 0.2s;
}

.article-card:hover {
  transform: translateX(4px);
}

.article-content h3 {
  font-size: 18px;
  margin-bottom: 8px;
  color: #303133;
}

.article-excerpt {
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid #ebeef5;
}

.author {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #606266;
}

.stats {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #909399;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}
</style>
