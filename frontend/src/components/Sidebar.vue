<template>
  <aside
    :class="[
      'fixed left-0 top-16 h-[calc(100vh-4rem)] flex flex-col bg-white dark:bg-gray-800 border-r dark:border-gray-700 transition-all duration-300 z-30',
      collapsed ? 'w-20' : 'w-64'
    ]"
  >
    <div class="flex items-center justify-between p-4 border-b dark:border-gray-700">
      <span v-if="!collapsed" class="font-bold text-lg text-blue-600">控制面板</span>
      <button @click="$emit('update:collapsed', !collapsed)"
              class="text-gray-500 hover:text-gray-700 dark:hover:text-gray-200 focus:outline-none">
        <i :class="collapsed ? 'fas fa-angle-right' : 'fas fa-angle-left'"></i>
      </button>
    </div>

    <div class="flex-1 overflow-y-auto px-2 py-3 space-y-1">
      <button
        v-for="item in items"
        :key="item.view"
        @click="$emit('navigate', item.view)"
        :class="[
          'flex items-center w-full text-left px-3 py-2 rounded-lg transition-colors',
          'hover:bg-blue-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200',
          activeView === item.view ? 'bg-blue-100 dark:bg-gray-700 font-semibold' : ''
        ]"
      >
        <i :class="['w-5 text-center text-blue-500', item.icon]"></i>
        <span v-if="!collapsed" class="ml-3 truncate">{{ item.label }}</span>
      </button>
    </div>

    <div class="border-t dark:border-gray-700 p-3">
      <p v-if="!collapsed" class="text-xs text-center text-gray-500 dark:text-gray-400 mt-2">© 2025 Polyglot Dict</p>
    </div>
  </aside>
</template>

<script setup>
defineProps({ collapsed: Boolean, activeView: String })
defineEmits(['update:collapsed', 'navigate'])

const items = [
  { label: '词汇管理', view: 'WordManager', icon: 'fas fa-book' },
  { label: '用户管理', view: 'UserManager', icon: 'fas fa-users' },
  { label: '操作日志', view: 'LogViewer', icon: 'fas fa-file-alt' },
]
</script>
