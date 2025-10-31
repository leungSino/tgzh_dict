<template>
  <div :class="['min-h-screen flex items-center justify-center p-4 transition-colors',
                theme.darkMode ? 'bg-gray-900' : 'bg-gray-50']">
    <div :class="['card w-full max-w-sm p-6 transition-colors',
                  theme.darkMode ? 'bg-gray-800 text-white' : 'bg-white text-gray-700']">
      <!-- 标题和返回按钮 -->
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-semibold">用户登录</h2>
        <button @click="$router.push('/')"
                class="text-blue-600 hover:underline text-sm">返回</button>
      </div>

      <!-- 表单 -->
      <form class="flex flex-col space-y-4" @submit.prevent="login">
        <!-- 用户名 -->
        <div class="flex flex-col">
          <input
            ref="usernameRef"
            v-model="username"
            type="text"
            placeholder="用户名"
            :class="['input transition-colors', theme.darkMode ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' : 'bg-white border-gray-300 text-gray-700 placeholder-gray-500']"
            @keyup.enter="login"
          />
          <p v-if="errors.username" class="text-red-500 text-sm mt-1">{{ errors.username }}</p>
        </div>

        <!-- 密码 -->
        <div class="flex flex-col">
          <input
            ref="passwordRef"
            v-model="password"
            type="password"
            placeholder="密码"
            :class="['input transition-colors', theme.darkMode ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' : 'bg-white border-gray-300 text-gray-700 placeholder-gray-500']"
            @keyup.enter="login"
          />
          <p v-if="errors.password" class="text-red-500 text-sm mt-1">{{ errors.password }}</p>
        </div>

        <!-- 登录按钮 -->
        <button
          type="submit"
          class="btn w-full py-2 text-lg"
          :disabled="loading"
        >
          {{ loading ? '登录中...' : '登录' }}
        </button>

        <!-- 服务器错误 -->
        <p v-if="errors.server" class="text-red-500 text-sm mt-2 text-center">{{ errors.server }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/userStore.js'
import { useThemeStore } from '../store/themeStore.js'

const router = useRouter()
const userStore = useUserStore()
const theme = useThemeStore()

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

  // 前端校验
  if (!username.value.trim()) errors.username = '用户名不能为空'
  else if (username.value.length < 3) errors.username = '用户名至少3个字符'

  if (!password.value.trim()) errors.password = '密码不能为空'
  else if (password.value.length < 4) errors.password = '密码至少4个字符'

  await nextTick()
  if (errors.username) {
    usernameRef.value.focus()
    return
  }
  if (errors.password) {
    passwordRef.value.focus()
    return
  }

  loading.value = true
  try {
    const ok = await userStore.login(username.value, password.value)
    if (ok) {
      router.push('/admin')
    } else {
      errors.server = '用户名或密码错误'
    }
  } catch {
    errors.server = '登录失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.input {
  @apply border px-3 py-2 rounded-lg w-full focus:outline-none focus:ring-2 focus:ring-blue-500 transition;
}
.btn {
  @apply bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition;
}
.card {
  @apply shadow-lg rounded-2xl p-6 w-full;
}
</style>
