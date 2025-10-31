<template>
  <div class="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900 transition-colors duration-300">

    <!-- 主体部分 -->
    <div class="flex flex-1 overflow-hidden">
      <!-- 移动端遮罩 -->
      <div
        v-if="sidebarOpen && isMobile"
        class="fixed inset-0 bg-black bg-opacity-50 z-20"
        @click="sidebarOpen = false"
      ></div>

      <!-- 左侧侧边栏 -->
      <Sidebar
        :open="sidebarOpen"
        :isMobile="isMobile"
        @navigate="handleNavigate"
      />

      <!-- 主体内容 -->
      <main class="flex-1 overflow-y-auto p-4 md:p-6 z-10">
        <component :is="currentView" />
      </main>
    </div>

    <!-- 底部（可选） -->
    <footer class="text-center py-3 text-gray-400 text-sm border-t dark:border-gray-700">
      © 2025 Polyglot Dict Admin Panel
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Navbar from './Navbar.vue'
import Sidebar from './Sidebar.vue'
import WordManager from './WordManager.vue'
import UserManager from './UserManager.vue'
import LogViewer from './LogViewer.vue'

const currentView = ref('WordManager')
const sidebarOpen = ref(false)
const isMobile = ref(window.innerWidth < 768)

const handleResize = () => {
  isMobile.value = window.innerWidth < 768
  if (!isMobile.value) sidebarOpen.value = true
}

const handleNavigate = (view) => {
  currentView.value = view
  if (isMobile.value) sidebarOpen.value = false
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
  handleResize()
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>
