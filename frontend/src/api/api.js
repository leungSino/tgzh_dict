import axios from 'axios'
import { useUserStore } from '../store/userStore.js'

const BASE_URL = 'http://localhost:8000'

// Axios 实例
const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000
})

// 请求拦截：自动加上 token
api.interceptors.request.use(config => {
  const store = useUserStore()
  if (store.token) {
    config.headers.Authorization = `Bearer ${store.token}`
  }
  return config
})

// -------------------
// 登录与注册
// -------------------
export async function login(username, password) {
  const res = await api.post('/auth/login', { username, password })
  return res.data
}

export async function register(username, password, role = 'editor') {
  const res = await api.post('/auth/register', { username, password, role })
  return res.data
}

// -------------------
// 用户管理
// -------------------

// 查询用户列表
export async function searchUsers(query = '', page = 1, pageSize = 10) {
  const res = await api.get('/admin/users', { params: { query, page, pageSize } })
  const list = res.data.data || res.data || []
  const total = res.data.total ?? list.length

  const items = list.map(u => ({
    ...u,
    id: u.id || u.username,
    created_at: u.created_at?.slice(0, 10) || '',
    updated_at: u.updated_at?.slice(0, 10) || ''
  }))
  return { items, total }
}

// 新增用户
export async function addUser(user) {
  const res = await api.post('/admin/users', user)
  return res.data
}

// 编辑用户
export async function updateUser(username, data) {
  const res = await api.put(`/admin/users/${username}`, data)
  return res.data
}

// 删除用户
export async function deleteUser(username) {
  const res = await api.delete(`/admin/users/${username}`)
  return res.data
}

// 启用/停用用户
export async function toggleUserStatus(username, currentStatus, updated_by = 'admin') {
  const newStatus = currentStatus === 'enabled' ? 'disabled' : 'enabled'
  const res = await updateUser(username, { status: newStatus, updated_by })
  return res
}

// 检查用户名是否存在
export async function checkUsername(username) {
  const res = await api.get('/admin/checkusername', {
    params: { username }
  })
  return res.data
}

// -------------------
// 翻译（Translations）管理
// -------------------
export async function getTranslations(query = '', page = 1, pageSize = 10) {
  const res = await api.get('/admin/translations', { params: { query, page, pageSize } })
  const list = res.data.data || res.data || []
  const total = res.data.total ?? list.length

  const items = list.map(t => ({
    ...t,
    id: t.id,
    sourceText: t.sourceText || '-',
    targetText: Object.values(t.translations || {}).map(v => v.translation).join('; '),
    lemma: t.lemma || '-',
    pos: t.pos || '-',
    tags: (t.tags || []).join(', ')
  }))
  return { items, total }
}

export async function addTranslation(data) {
  const res = await api.post('/admin/translations', data)
  return res.data
}

export async function updateTranslation(id, data) {
  const res = await api.put(`/admin/translations/${id}`, data)
  return res.data
}

export async function deleteTranslation(id) {
  const res = await api.delete(`/admin/translations/${id}`)
  return res.data
}

// -------------------
// 原型词（Lemmas）管理
// -------------------
export async function getLemmas(query = '', page = 1, pageSize = 10) {
  const res = await api.get('/admin/lemmas', { params: { query, page, pageSize } })
  const list = res.data.data || res.data || []
  const total = res.data.total ?? list.length

  const items = list.map(l => ({
    ...l,
    id: l.id,
    definition: l.definition?.zh || l.definition?.en || '-',
    derived: (l.derived || []).join(', '),
    lemma: l.lemma || '-',
    root: l.root || '-',
    pos: l.pos || '-'
  }))
  return { items, total }
}

export async function addLemma(data) {
  const res = await api.post('/admin/lemmas', data)
  return res.data
}

export async function updateLemma(id, data) {
  const res = await api.put(`/admin/lemmas/${id}`, data)
  return res.data
}

export async function deleteLemma(id) {
  const res = await api.delete(`/admin/lemmas/${id}`)
  return res.data
}

// -------------------
// 单词（Words）管理
// -------------------
export async function getWords() {
  const res = await api.get('/admin/words')
  return { data: res.data || [] }
}

export async function addWord(payload) {
  const res = await api.post('/admin/words', payload)
  return res.data
}

export async function updateWord(id, payload) {
  const res = await api.put(`/admin/words/${id}`, payload)
  return res.data
}

export async function deleteWord(id) {
  const res = await api.delete(`/admin/words/${id}`)
  return res.data
}

export async function searchWords(q = '', lang = 'zh') {
  const res = await api.get('/admin/words/search', { params: { q, lang } })
  return { data: res.data || [] }
}

// -------------------
// 操作日志（Logs）管理
// -------------------
// 日志接口：标准化返回 { items, total }
export async function getLogs(query = '', page = 1, pageSize = 10) {
  try {
    const res = await api.get(`/admin/logs`, {
      params: { query, page, pageSize }
    })
    const items = Array.isArray(res.data?.items) ? res.data.items : []
    const total = res.data?.total || items.length
    return { items, total }
  } catch (err) {
    console.error('获取日志失败:', err)
    return { items: [], total: 0 }
  }
}

export async function deleteLog(id) {
  const res = await api.delete(`/admin/logs/${id}`)
  return res.data
}

export async function clearLogs() {
  const res = await api.delete('/admin/logs')
  return res.data
}

export async function getStats() {
  const res = await api.get('/admin/logs/stats')
  return res.data
}

// -------------------
// 默认导出
// -------------------
export default {
  // Auth
  login,
  register,

  // Users
  searchUsers,
  addUser,
  updateUser,
  deleteUser,
  toggleUserStatus,
  checkUsername,

  // Words
  getWords,
  addWord,
  updateWord,
  deleteWord,
  searchWords,

  // Translations
  getTranslations,
  addTranslation,
  updateTranslation,
  deleteTranslation,

  // Lemmas
  getLemmas,
  addLemma,
  updateLemma,
  deleteLemma,

  // Logs
  getLogs,
  deleteLog,
  clearLogs,
  getStats
}
