import { defineStore } from 'pinia'
import api from '../api'

export const useAdminStore = defineStore('admin', {
  state: () => ({
    token: localStorage.getItem('admin_token') || null,
    username: null,
    stats: null
  }),

  getters: {
    isLoggedIn: (state) => !!state.token
  },

  actions: {
    async login(username, password) {
      const response = await api.post('/admin/login', { username, password })
      this.token = response.data.access_token
      this.username = 'admin'
      localStorage.setItem('admin_token', this.token)
      return response.data
    },

    logout() {
      this.token = null
      this.username = null
      this.stats = null
      localStorage.removeItem('admin_token')
    },

    async fetchStats() {
      const response = await api.get('/admin/stats', {
        headers: { 'X-Admin-Token': this.token }
      })
      this.stats = response.data
      return response.data
    },

    async fetchUsers(params = {}) {
      const response = await api.get('/admin/users', {
        headers: { 'X-Admin-Token': this.token },
        params
      })
      return response.data
    },

    async toggleUserAdmin(userId) {
      const response = await api.put(`/admin/users/${userId}/toggle-admin`, {}, {
        headers: { 'X-Admin-Token': this.token }
      })
      return response.data
    },

    async toggleUserActive(userId) {
      const response = await api.put(`/admin/users/${userId}/toggle-active`, {}, {
        headers: { 'X-Admin-Token': this.token }
      })
      return response.data
    },

    async deleteUser(userId) {
      const response = await api.delete(`/admin/users/${userId}`, {
        headers: { 'X-Admin-Token': this.token }
      })
      return response.data
    },

    async fetchGames(params = {}) {
      const response = await api.get('/admin/games', {
        headers: { 'X-Admin-Token': this.token },
        params
      })
      return response.data
    },

    async createGame(game) {
      const response = await api.post('/admin/games', game, {
        headers: { 'X-Admin-Token': this.token }
      })
      return response.data
    },

    async updateGame(gameId, game) {
      const response = await api.put(`/admin/games/${gameId}`, game, {
        headers: { 'X-Admin-Token': this.token }
      })
      return response.data
    },

    async deleteGame(gameId) {
      const response = await api.delete(`/admin/games/${gameId}`, {
        headers: { 'X-Admin-Token': this.token }
      })
      return response.data
    },

    async fetchArticles(params = {}) {
      const response = await api.get('/admin/articles', {
        headers: { 'X-Admin-Token': this.token },
        params
      })
      return response.data
    },

    async toggleArticlePublished(articleId) {
      const response = await api.put(`/admin/articles/${articleId}/toggle-published`, {}, {
        headers: { 'X-Admin-Token': this.token }
      })
      return response.data
    },

    async deleteArticle(articleId) {
      const response = await api.delete(`/admin/articles/${articleId}`, {
        headers: { 'X-Admin-Token': this.token }
      })
      return response.data
    },

    // 数据统计相关
    async fetchTopGames(limit = 5) {
      const response = await api.get('/admin/rankings/games', {
        headers: { 'X-Admin-Token': this.token },
        params: { limit }
      })
      return response.data
    },

    async fetchTopArticles(limit = 5) {
      const response = await api.get('/admin/rankings/articles', {
        headers: { 'X-Admin-Token': this.token },
        params: { limit }
      })
      return response.data
    },

    async fetchViewsTrend(days = 7) {
      const response = await api.get('/admin/rankings/trend', {
        headers: { 'X-Admin-Token': this.token },
        params: { days }
      })
      return response.data
    },

    async fetchArticleCategories() {
      const response = await api.get('/admin/rankings/categories', {
        headers: { 'X-Admin-Token': this.token }
      })
      return response.data
    },

    async cleanupAnalyticsData() {
      const response = await api.post('/admin/analytics/cleanup', {}, {
        headers: { 'X-Admin-Token': this.token }
      })
      return response.data
    },

    async verifyAnalyticsData() {
      const response = await api.get('/admin/analytics/verify', {
        headers: { 'X-Admin-Token': this.token }
      })
      return response.data
    },

    async fetchAnalyticsSummary(days = 7) {
      const response = await api.get('/analytics/summary', {
        headers: { 'X-Admin-Token': this.token },
        params: { days }
      })
      return response.data
    }
  }
})
