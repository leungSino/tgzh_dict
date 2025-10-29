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
          return false
        }
      } catch {
        this.logout()
        return false
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
    // 页面刷新时调用
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
