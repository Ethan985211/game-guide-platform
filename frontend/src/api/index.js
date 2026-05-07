import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// 添加请求拦截器，自动携带token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const gameAPI = {
  getGames: (params) => api.get('/games', { params }),
  getGame: (id) => api.get(`/games/${id}`),
  getGameCharacters: (gameId) => api.get(`/games/${gameId}/characters`)
}

export const articleAPI = {
  getArticles: (params) => api.get('/articles', { params }),
  getArticle: (id) => api.get(`/articles/${id}`),
  createArticle: (data) => api.post('/articles', data),
  updateArticle: (id, data) => api.put(`/articles/${id}`, data),
  deleteArticle: (id) => api.delete(`/articles/${id}`),
  likeArticle: (id) => api.post(`/articles/${id}/like`)
}

export const characterAPI = {
  getCharacters: (params) => api.get('/characters', { params }),
  getCharacter: (id) => api.get(`/characters/${id}`)
}

export const commentAPI = {
  getComments: (articleId) => api.get(`/comments/article/${articleId}`),
  createComment: (data) => api.post('/comments', data),
  deleteComment: (id) => api.delete(`/comments/${id}`),
  likeComment: (id) => api.post(`/comments/${id}/like`)
}

export const searchAPI = {
  search: (q, type) => api.get('/search', { params: { q, type } })
}

export default api
