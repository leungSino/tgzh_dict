<template>
  <div class="flex h-screen bg-gray-50 dark:bg-gray-900 overflow-hidden pt-16">
    <!-- Sidebar -->
    <Sidebar
      v-model:collapsed="sidebarCollapsed"
      :activeView="activeTab"
      @navigate="activeTab = $event"
    />

    <!-- 主内容 -->
    <main class="flex-1 overflow-auto transition-all duration-300"
          :class="sidebarCollapsed ? 'ml-20' : 'ml-64'">
      <component :is="activeTabComponent" class="p-4"/>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import WordManager from '../components/WordManager.vue'
import UserManager from '../components/UserManager.vue'
import LogViewer from '../components/LogViewer.vue'

const activeTab = ref('WordManager')
const sidebarCollapsed = ref(false)

const activeTabComponent = computed(() => {
  switch(activeTab.value){
    case 'WordManager': return WordManager
    case 'UserManager': return UserManager
    case 'LogViewer': return LogViewer
    default: return WordManager
  }
})
</script>
