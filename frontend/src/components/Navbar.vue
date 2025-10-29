<template>
  <nav class="bg-white shadow-sm px-6 py-4 flex justify-between items-center">
    <h1 class="text-xl font-semibold text-blue-600 cursor-pointer" @click="goHome">
      Polyglot Dict
    </h1>

    <div>
      <!-- 游客 -->
      <button
        v-if="!user.isLoggedIn || user.role === 'guest'"
        @click="goLogin"
        class="text-blue-600 font-medium hover:underline"
      >
        登录
      </button>

      <!-- 已登录用户 -->
      <div v-else class="flex items-center space-x-4">
        <span class="text-gray-700">{{ user.username }}（{{ user.role }}）</span>
        <button @click="logout" class="text-red-500 hover:underline">退出</button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/userStore.js'

const router = useRouter()
const user = useUserStore()

const goLogin = () => router.push('/login')
const goHome = () => router.push('/')
const logout = () => {
  user.logout()
  router.push('/')
}
</script>

<style>
/* 可选：导航栏样式 */
</style>
