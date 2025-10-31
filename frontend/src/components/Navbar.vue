<template>
  <nav
    :class="[
      'bg-white shadow-sm px-6 py-4 flex justify-between items-center',
      theme.darkMode ? 'bg-gray-900 text-white' : 'bg-white text-gray-700'
    ]"
  >
    <h1 class="text-xl font-semibold text-blue-600 cursor-pointer">
      Polyglot Dict
    </h1>

    <div class="flex items-center space-x-4">
      <!-- 在 Navbar 的已登录用户部分，添加切换按钮 -->
      <button v-if="user.isLoggedIn" @click="toggleAdminView"
        class="text-blue-600 dark:text-blue-400 font-medium hover:underline">
        {{ onQueryPage ? '返回管理' : '去查询' }}
      </button>

      <!-- 切换主题 -->
      <button
        @click="theme.toggleTheme"
        class="px-2 py-1 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-200 text-sm"
      >
        {{ theme.darkMode ? '🌙 暗' : '☀️ 亮' }}
      </button>

      <!-- 游客 -->
      <button
        v-if="!user.isLoggedIn || user.role === 'guest'"
        @click="goLogin"
        class="text-blue-600 dark:text-blue-400 font-medium hover:underline"
      >
        登录
      </button>

      <!-- 已登录用户 -->
      <div v-else class="flex items-center space-x-4">
        <span :class="theme.darkMode ? 'text-gray-300' : 'text-gray-700'">
          {{ user.username }}（{{ user.role }}）
        </span>
        <button @click="logout" class="text-red-500 hover:underline">退出</button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/userStore.js'
import { useThemeStore } from '../store/themeStore.js'
import { ref } from 'vue'

const router = useRouter()
const user = useUserStore()
const theme = useThemeStore()

const onQueryPage = ref(false)
const toggleAdminView = () => {
  if (onQueryPage.value) {
    router.push('/admin')
    onQueryPage.value = false
  } else {
    router.push('/')
    onQueryPage.value = true
  }
}

const goLogin = () => router.push('/login')
const goHome = () => router.push('/')
const logout = () => {
  user.logout()
  router.push('/')
}
</script>
