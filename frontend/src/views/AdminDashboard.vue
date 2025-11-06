<template>
  <div class="flex h-screen bg-gray-50 dark:bg-gray-900">
    <Sidebar v-model:collapsed="sidebarCollapsed" :activeView="activeTab" @navigate="activeTab = $event" />

    <main class="flex-1 transition-all duration-300 overflow-auto pt-16"
          :class="sidebarCollapsed ? 'ml-20' : 'ml-64'">
      <div class="p-1">
        <component :is="activeTabComponent" />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import WordManager from '@/components/WordManager.vue'
import UserManager from '@/components/UserManager.vue'
import LogManager from '@/components/LogManager.vue'

const activeTab = ref('WordManager')
const sidebarCollapsed = ref(false)

const activeTabComponent = computed(() => {
  switch (activeTab.value) {
    case 'WordManager': return WordManager
    case 'UserManager': return UserManager
    case 'LogManager': return LogManager
    default: return WordManager
  }
})
</script>
