<template>
  <nav
    class="fixed top-0 left-0 w-full h-16 shadow-sm px-4 sm:px-6 flex justify-between items-center transition-colors z-50"
    :class="theme.darkMode ? 'bg-gray-900 text-white' : 'bg-white text-gray-700'"
  >
    <!-- 左侧标题 -->
    <h1
      class="text-xl font-bold text-blue-600 cursor-pointer select-none hover:text-blue-500 transition-colors"
      @click="router.push('/')"
    >
      Polyglot Dict
    </h1>

    <!-- 右侧按钮组 -->
    <div class="flex items-center space-x-2 sm:space-x-4">
      <!-- 切换主题 -->
      <button
        @click="theme.toggleTheme"
        class="px-3 py-1 rounded-lg border border-gray-300 dark:border-gray-600 text-sm transition-colors hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center justify-center"
      >
        {{ theme.darkMode ? '🌙 暗' : '☀️ 亮' }}
      </button>

      <!-- 大屏幕按钮组 -->
      <template v-if="user.isLoggedIn">
        <!-- 管理页切换 -->
        <button
          v-if="['admin','editor'].includes(user.role)"
          class="hidden sm:flex px-3 py-1 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors items-center justify-center"
          @click="togglePage"
        >
          <i class="fas fa-exchange-alt mr-1"></i>
          <span>{{ onAdminPage ? '去查询' : '返回管理' }}</span>
        </button>

        <!-- 用户信息 -->
        <div
          v-if="user.role !== 'guest'"
          class="hidden sm:flex px-3 py-1 border rounded-lg border-gray-300 dark:border-gray-600 text-sm text-gray-700 dark:text-gray-200 items-center space-x-1"
        >
          <i class="fas fa-user-circle"></i>
          <span>{{ user.username }}（{{ user.role }}）</span>
        </div>

        <!-- 退出按钮 -->
        <button
          v-if="user.role !== 'guest'"
          class="hidden sm:flex px-3 py-1 text-red-500 text-sm font-medium hover:underline transition-colors"
          @click="logout"
        >
          退出
        </button>
      </template>

      <!-- 游客登录按钮 -->
      <button
        v-if="!user.isLoggedIn || user.role === 'guest'"
        class="hidden sm:flex px-3 py-1 text-blue-600 dark:text-blue-400 text-sm font-medium hover:underline transition-colors"
        @click="goLogin"
      >
        登录
      </button>

      <!-- 移动端汉堡菜单 -->
      <div class="sm:hidden relative" ref="menuContainer">
        <button
          @click="mobileMenuOpen = !mobileMenuOpen"
          class="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
        >
          <i class="fas fa-bars"></i>
        </button>

        <!-- 移动端浮层菜单 -->
        <div
          v-if="mobileMenuOpen"
          class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg shadow-lg z-50 flex flex-col"
        >
          <template v-if="user.isLoggedIn && ['admin','editor'].includes(user.role)">
            <button
              @click="onMobileTogglePage"
              class="flex items-center px-3 py-2 hover:bg-blue-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200"
            >
              <i class="fas fa-exchange-alt mr-2"></i>
              {{ onAdminPage ? '去查询' : '返回管理' }}
            </button>

            <div class="px-3 py-2 border-t border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-200 flex items-center space-x-2">
              <i class="fas fa-user-circle text-lg"></i>
              <span>{{ user.username }}（{{ user.role }}）</span>
            </div>

            <button
              @click="onMobileLogout"
              class="px-3 py-2 text-red-500 hover:underline text-left"
            >
              退出
            </button>
          </template>

          <template v-else>
            <button
              @click="onMobileLogin"
              class="px-3 py-2 text-blue-600 dark:text-blue-400 hover:underline text-left"
            >
              登录
            </button>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../store/userStore.js'
import { useThemeStore } from '../store/themeStore.js'

const router = useRouter()
const route = useRoute()
const user = useUserStore()
const theme = useThemeStore()

const mobileMenuOpen = ref(false)
const menuContainer = ref(null)

const onAdminPage = computed(() => route.path.startsWith('/admin'))

const togglePage = () => {
  if (onAdminPage.value) router.push('/')
  else router.push('/admin')
}

const goLogin = () => router.push('/login')
const logout = () => {
  user.logout()
  router.push('/')
  mobileMenuOpen.value = false
}

// 移动端安全方法
const onMobileTogglePage = () => {
  togglePage()
  mobileMenuOpen.value = false
}
const onMobileLogout = () => {
  logout()
}
const onMobileLogin = () => {
  goLogin()
  mobileMenuOpen.value = false
}

// 点击页面其他地方关闭移动端菜单
const handleClickOutside = (e) => {
  if (menuContainer.value && !menuContainer.value.contains(e.target)) {
    mobileMenuOpen.value = false
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', handleClickOutside))
</script>
