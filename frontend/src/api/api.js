import axios from 'axios'
import { useUserStore } from '../store/userStore.js'

const BASE = 'http://localhost:8000'
const instance = axios.create({ baseURL: BASE, timeout: 10000 })

instance.interceptors.request.use(cfg => {
  const store = useUserStore()
  if (store.token) cfg.headers.Authorization = `Bearer ${store.token}`
  return cfg
})

// 用户相关
export async function login(username, password) {
  const res = await instance.post('/auth/login', { username, password })
  return res.data
}

export async function register(username, password, role = 'editor') {
  const res = await instance.post('/auth/register', { username, password, role })
  return res.data
}

// 词汇相关 API
export async function addWord(payload) {
  const res = await instance.post('/api/words/', payload)
  return { ...res.data, id: res.data._id }
}

export async function updateWord(id, payload) {
  const res = await instance.put(`/api/words/${id}`, payload)
  return { ...res.data, id: res.data._id }
}

export async function deleteWord(id) {
  if (!id) throw new Error("Invalid word id")
  const res = await instance.delete(`/api/words/${id}`)
  return res.data
  //return instance.delete(`/api/words/${id}`)
}

export async function getWords() {
  const res = await instance.get('/api/words/')
  return {
    data: (res.data || []).map(item => ({ ...item, id: item.id }))
  }
}

export async function searchWords(q = '', lang = 'zh') {
  const res = await instance.get('/api/words/search/', { params: { q, lang } })
  return {
    data: (res.data || []).map(item => ({ ...item, id: item.id }))
  }
}

// 日志与统计
export async function getLogs() { return instance.get('/admin/logs') }
export async function getStats() { return instance.get('/admin/logs/stats') }

export default {
  login,
  register,
  addWord,
  updateWord,
  deleteWord,
  getWords,
  searchWords,
  getLogs,
  getStats
}
