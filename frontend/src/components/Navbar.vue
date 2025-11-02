<template>
  <nav
    :class="[
      'shadow-sm px-6 py-4 flex justify-between items-center transition-colors',
      theme.darkMode ? 'bg-gray-900 text-white' : 'bg-white text-gray-700'
    ]"
  >
    <!-- 左侧标题 -->
    <h1 class="text-xl font-semibold text-blue-600 cursor-pointer select-none">
      Polyglot Dict
    </h1>

    <!-- 右侧按钮组 -->
    <div class="flex items-center space-x-4">
      <!-- 切换主题按钮 -->
      <button
        @click="theme.toggleTheme"
        class="px-2 py-1 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-200 text-sm"
      >
        {{ theme.darkMode ? '🌙 暗' : '☀️ 亮' }}
      </button>

      <!-- 仅登录用户显示 -->
      <template v-if="user.isLoggedIn && user.role !== 'guest'">
        <button
          @click="togglePage"
          class="text-blue-600 dark:text-blue-400 font-medium hover:underline"
        >
          {{ onAdminPage ? '去查询' : '返回管理' }}
        </button>
        <span :class="theme.darkMode ? 'text-gray-300' : 'text-gray-700'">
          {{ user.username }}（{{ user.role }}）
        </span>
        <button @click="logout" class="text-red-500 hover:underline">退出</button>
      </template>

      <!-- 游客登录按钮 -->
      <button
        v-else
        @click="goLogin"
        class="text-blue-600 dark:text-blue-400 font-medium hover:underline"
      >
        登录
      </button>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../store/userStore.js'
import { useThemeStore } from '../store/themeStore.js'

const router = useRouter()
const route = useRoute()
const user = useUserStore()
const theme = useThemeStore()

// 当前是否在管理页
const onAdminPage = computed(() => route.path.startsWith('/admin'))

// 跳转逻辑：在管理页 -> 去查询；在查询页 -> 返回管理
const togglePage = () => {
  if (onAdminPage.value) {
    router.push('/')
  } else {
    router.push('/admin')
  }
}

// 其他按钮
const goLogin = () => router.push('/login')
const logout = () => {
  user.logout()
  router.push('/')
}
</script>

<style scoped>
nav {
  @apply transition-colors duration-300;
}
</style>
