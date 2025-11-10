import { defineStore } from 'pinia'
import api from '../api/api.js'

export const useUserStore = defineStore('user', {
  state: () => ({
    username: '',
    role: 'guest',
    token: '',
    isLoggedIn: false
  }),
  actions: {
    async login(username, password) {
      try {
        const res = await api.login(username, password)
        if (res.access_token) {
          this.username = username
          this.role = res.role || 'editor'
          this.token = res.access_token
          this.isLoggedIn = true
          // 存储到 localStorage
          localStorage.setItem('token', this.token)
          localStorage.setItem('username', this.username)
          localStorage.setItem('role', this.role)
          return true
        } else {
          this.logout()
          // 如果后端有 detail，透传
          return res?.detail || false
        }
      } catch (err) {
        this.logout()
        // 返回后端错误信息
        return err.response?.data || false
      }
    },
    logout() {
      this.username = ''
      this.role = 'guest'
      this.token = ''
      this.isLoggedIn = false
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('role')
    },
    restore() {
      const token = localStorage.getItem('token')
      const username = localStorage.getItem('username')
      const role = localStorage.getItem('role')
      if (token && username && role) {
        this.token = token
        this.username = username
        this.role = role
        this.isLoggedIn = true
      }
    }
  }
})
