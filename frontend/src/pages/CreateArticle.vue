<template>
  <div class="create-article page-container">
    <h1 class="page-title">发布文章</h1>

    <el-card>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="输入文章标题" />
        </el-form-item>

        <el-form-item label="关联游戏" prop="game_id">
          <el-select v-model="form.game_id" placeholder="选择关联游戏（可选）" clearable filterable>
            <el-option v-for="game in games" :key="game.id" :label="game.name" :value="game.id" />
          </el-select>
        </el-form-item>

        <el-form-item label="分类" prop="category">
          <el-select v-model="form.category" placeholder="选择文章类型">
            <el-option label="攻略" value="guide" />
            <el-option label="资讯" value="news" />
            <el-option label="技巧" value="tips" />
          </el-select>
        </el-form-item>

        <el-form-item label="标签" prop="tags">
          <el-input v-model="form.tags" placeholder="多个标签用逗号分隔" />
        </el-form-item>

        <el-form-item label="内容" prop="content">
          <div style="margin-bottom: 8px;">
            <input
              ref="imageInput"
              type="file"
              accept="image/jpeg,image/png,image/gif,image/webp"
              style="display: none;"
              @change="handleImageUpload"
            />
            <el-button size="small" @click="$refs.imageInput.click()" :loading="uploading">
              📷 插入图片
            </el-button>
            <span style="margin-left: 8px; font-size: 12px; color: #999;">支持 JPG/PNG/GIF/WebP，最大 10MB</span>
          </div>
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="15"
            placeholder="输入文章内容（支持 Markdown，图片用 ![](url) 语法）"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="loading">发布文章</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { gameAPI, articleAPI } from '../api'

const router = useRouter()
const formRef = ref()
const games = ref([])
const loading = ref(false)
const uploading = ref(false)
const imageInput = ref(null)

const form = ref({
  title: '',
  slug: '',
  content: '',
  game_id: null,
  category: 'guide',
  tags: ''
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }]
}

const loadGames = async () => {
  try {
    const response = await gameAPI.getGames({ limit: 100 })
    games.value = response.data
  } catch (error) {
    console.error('加载游戏失败', error)
  }
}

const handleImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  // 校验类型和大小
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
  if (!allowedTypes.includes(file.type)) {
    ElMessage.error('不支持的图片类型，仅支持 JPG/PNG/GIF/WebP')
    return
  }
  if (file.size > 10 * 1024 * 1024) {
    ElMessage.error('图片大小不能超过 10MB')
    return
  }

  uploading.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/upload/image', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    // 插入 Markdown 图片语法
    const imgMarkdown = `![${file.name}](${response.data.url})`
    form.value.content = form.value.content + '\n' + imgMarkdown + '\n'
    ElMessage.success('图片上传成功，已插入到文章末尾')
  } catch (err) {
    const detail = err.response?.data?.detail
    ElMessage.error(detail || '图片上传失败')
  } finally {
    uploading.value = false
    // 重置 input，允许重复上传同一文件
    event.target.value = ''
  }
}

const submitForm = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    // 生成slug
    const slug = form.value.title.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]/g, '')

    await articleAPI.createArticle({
      ...form.value,
      slug: `${slug}-${Date.now()}`
    })
    ElMessage.success('发布成功')
    router.push('/articles')
  } catch (error) {
    ElMessage.error('发布失败')
  } finally {
    loading.value = false
  }
}

onMounted(loadGames)
</script>

<style scoped>
.create-article {
  padding-top: 20px;
  max-width: 900px;
}
</style>
