<template>
  <div class="min-h-screen flex items-center justify-center p-4 bg-gray-50 dark:bg-gray-900">
    <div class="w-full max-w-sm p-6 bg-white dark:bg-gray-800 rounded-2xl shadow-lg text-gray-700 dark:text-white">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-semibold">用户登录</h2>
        <button @click="$router.push('/')" class="text-blue-600 hover:underline text-sm">返回</button>
      </div>

      <form class="flex flex-col space-y-4" @submit.prevent="login">
        <input ref="usernameRef" v-model="username" type="text" placeholder="用户名"
               class="border px-3 py-2 rounded-lg w-full bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"/>
        <p v-if="errors.username" class="text-red-500 text-sm">{{ errors.username }}</p>

        <input ref="passwordRef" v-model="password" type="password" placeholder="密码"
               class="border px-3 py-2 rounded-lg w-full bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"/>
        <p v-if="errors.password" class="text-red-500 text-sm">{{ errors.password }}</p>

        <button type="submit" :disabled="loading" class="bg-blue-600 text-white rounded-lg py-2 px-4 hover:bg-blue-700">
          {{ loading ? '登录中...' : '登录' }}
        </button>

        <p v-if="errors.server" class="text-red-500 text-sm text-center">{{ errors.server }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/userStore.js'

const router = useRouter()
const userStore = useUserStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const errors = reactive({ username: '', password: '', server: '' })

const usernameRef = ref(null)
const passwordRef = ref(null)

const login = async () => {
  errors.username = ''
  errors.password = ''
  errors.server = ''

  if (!username.value.trim()) errors.username = '用户名不能为空'
  if (!password.value.trim()) errors.password = '密码不能为空'
  await nextTick()
  if (errors.username) { usernameRef.value.focus(); return }
  if (errors.password) { passwordRef.value.focus(); return }

  loading.value = true
  try {
    const ok = await userStore.login(username.value, password.value)
    if (ok) router.push('/admin')
    else errors.server = '用户名或密码错误'
  } catch {
    errors.server = '登录失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* 可选局部样式 */
</style>
