<template>
  <div class="flex h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Sidebar -->
    <Sidebar
      v-model:collapsed="sidebarCollapsed"
      :activeView="activeTab"
      :items="filteredItems"
      :auto-collapse-breakpoint="768"
      @navigate="handleNavigate"
    />

    <!-- 主内容 -->
    <main
      class="flex-1 transition-margin duration-300 overflow-auto pt-16"
      :class="sidebarCollapsed ? 'ml-20' : 'ml-64'"
      style="backface-visibility: hidden; transform: translateZ(0);"
    >
      <div class="p-4">
        <component :is="activeTabComponent" />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, watchEffect, onMounted, onUnmounted } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import WordManager from '@/components/WordManager.vue'
import UserManager from '@/components/UserManager.vue'
import LogManager from '@/components/LogManager.vue'
import { useUserStore } from '@/store/userStore.js'

const userStore = useUserStore()
const role = computed(() => userStore.role || 'editor')

const sidebarCollapsed = ref(false)

// 完整菜单
const items = [
  { label: '词汇管理', view: 'WordManager', icon: 'fas fa-book' },
  { label: '用户管理', view: 'UserManager', icon: 'fas fa-users' },
  { label: '操作日志', view: 'LogManager', icon: 'fas fa-file-alt' },
]

// 权限表
const allowedTabs = {
  admin: ['WordManager', 'UserManager', 'LogManager'],
  editor: ['WordManager']
}

// 根据角色过滤 Sidebar 显示的菜单
const filteredItems = computed(() =>
  items.filter(i => allowedTabs[role.value]?.includes(i.view))
)

// activeTab 初始化为第一个允许访问的菜单
const activeTab = ref(filteredItems.value[0]?.view || 'WordManager')

// 点击切换
function handleNavigate(tab) {
  if (allowedTabs[role.value]?.includes(tab)) {
    activeTab.value = tab
  } else {
    alert('您没有权限访问此功能')
  }
}

// 根据 activeTab 显示组件
const activeTabComponent = computed(() => {
  switch (activeTab.value) {
    case 'WordManager':
      return WordManager
    case 'UserManager':
      return UserManager
    case 'LogManager':
      return LogManager
    default:
      return WordManager
  }
})

// 当 role 变化时，确保 activeTab 仍合法
watchEffect(() => {
  if (!allowedTabs[role.value]?.includes(activeTab.value)) {
    activeTab.value = filteredItems.value[0]?.view || 'WordManager'
  }
})

// 响应式处理：在移动端默认折叠
const checkScreenSize = () => {
  if (window.innerWidth < 768 && !sidebarCollapsed.value) {
    sidebarCollapsed.value = true
  }
}

onMounted(() => {
  checkScreenSize()
  window.addEventListener('resize', checkScreenSize)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkScreenSize)
})
</script>