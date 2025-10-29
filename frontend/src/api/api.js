import axios from 'axios'
import { useUserStore } from '../store/userStore.js'

const BASE = 'http://localhost:8000'
const instance = axios.create({ baseURL: BASE, timeout: 10000 })

instance.interceptors.request.use(cfg => {
  const store = useUserStore()
  if (store.token) cfg.headers.Authorization = `Bearer ${store.token}`
  return cfg
})

export async function login(username, password) {
  const res = await instance.post('/auth/login', { username, password })
  return res.data
}

// 其他 API
export async function register(username, password, role = 'editor') {
  const res = await instance.post('/auth/register', { username, password, role })
  return res.data
}

export async function addWord(payload) { return instance.post('/api/words/', payload) }
export async function searchWords(q, lang='zh') { return instance.get('/api/words/search/', { params: { q, lang } }) }
export async function deleteWord(id) { return instance.delete(`/api/words/${id}`) }
export async function getLogs() { return instance.get('/admin/logs') }
export async function getStats() { return instance.get('/admin/logs/stats') }
export default {
  login,
  register,
  addWord,
  searchWords,
  deleteWord,
  getLogs,
  getStats
}
