import { defineStore } from 'pinia'
import axios from 'axios'

const api = axios.create({
  baseURL: '/api'
})

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null
  }),

  getters: {
    isLoggedIn: (state) => !!state.token
  },

  actions: {
    async login(email, password) {
      const formData = new FormData()
      formData.append('username', email)
      formData.append('password', password)

      const response = await api.post('/auth/login', formData)
      this.token = response.data.access_token
      localStorage.setItem('token', this.token)
      api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
      await this.fetchUser()
      return response.data
    },

    async register(username, email, password) {
      const response = await api.post('/auth/register', {
        username,
        email,
        password
      })
      return response.data
    },

    async fetchUser() {
      if (!this.token) return
      api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
      try {
        const response = await api.get('/auth/me')
        this.user = response.data
      } catch (error) {
        this.logout()
      }
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      delete api.defaults.headers.common['Authorization']
    }
  }
})
