<template>
  <aside
    :class="[
      'fixed left-0 top-16 bottom-0 flex flex-col bg-white dark:bg-gray-800 border-r dark:border-gray-700 z-30',
      'transition-[width] duration-300 ease-out',
      collapsed ? 'w-20' : 'w-64'
    ]"
  >
    <!-- 顶部区域 - 使用固定布局确保按钮始终可见 -->
    <div class="flex items-center p-4 border-b dark:border-gray-700 h-16 relative">
      <!-- 标题 - 只在展开时显示 -->
      <div
        class="transition-opacity duration-300 overflow-hidden"
        :class="collapsed ? 'opacity-0 w-0' : 'opacity-100 w-auto'"
      >
        <span class="font-bold text-lg text-blue-600 whitespace-nowrap">
          控制面板
        </span>
      </div>

      <!-- 折叠按钮 - 绝对定位，始终在右上角 -->
      <button
        @click="toggleCollapse"
        class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 dark:hover:text-gray-200 focus:outline-none w-6 h-6 flex items-center justify-center bg-white dark:bg-gray-800 rounded-md border border-gray-200 dark:border-gray-600 shadow-sm"
        :title="collapsed ? '展开侧边栏' : '折叠侧边栏'"
      >
        <i :class="collapsed ? 'fas fa-angle-right text-sm' : 'fas fa-angle-left text-sm'"></i>
      </button>
    </div>

    <!-- 菜单列表 -->
    <div class="flex-1 overflow-y-auto px-2 py-3 space-y-1">
      <button
        v-for="item in items"
        :key="item.view"
        @click="handleItemClick(item.view)"
        :class="[
          'flex items-center w-full text-left px-3 py-2 rounded-lg transition-colors',
          'hover:bg-blue-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200',
          activeView === item.view ? 'bg-blue-100 dark:bg-gray-700 font-semibold' : ''
        ]"
      >
        <i :class="['w-5 text-center text-blue-500 flex-shrink-0', item.icon]"></i>
        <span
          class="transition-opacity duration-300 truncate"
          :class="collapsed ? 'opacity-0 ml-0' : 'opacity-100 ml-3'"
        >
          {{ item.label }}
        </span>
      </button>
    </div>

    <!-- 底部版权 -->
    <div class="border-t dark:border-gray-700 p-3">
      <p
        class="text-xs text-center text-gray-500 dark:text-gray-400 transition-opacity duration-300"
        :class="collapsed ? 'opacity-0' : 'opacity-100'"
      >
        © 2025 Polyglot Dict
      </p>
    </div>

    <!-- 移动端遮罩 -->
    <div
      v-if="isMobile && !collapsed"
      class="fixed inset-0 bg-black bg-opacity-50 z-20 md:hidden"
      @click="handleMaskClick"
    ></div>
  </aside>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  collapsed: Boolean,
  activeView: String,
  items: {
    type: Array,
    default: () => []
  },
  autoCollapseBreakpoint: {
    type: Number,
    default: 768
  }
})

const emit = defineEmits(['update:collapsed', 'navigate'])

// 响应式状态
const isMobile = ref(false)

// 检查屏幕尺寸
const checkScreenSize = () => {
  const mobile = window.innerWidth < props.autoCollapseBreakpoint
  if (mobile !== isMobile.value) {
    isMobile.value = mobile
    if (mobile && !props.collapsed) {
      emit('update:collapsed', true)
    }
  }
}

// 切换折叠状态
const toggleCollapse = () => {
  console.log('Toggle button clicked, current state:', props.collapsed)
  emit('update:collapsed', !props.collapsed)
}

// 处理菜单项点击
const handleItemClick = (view) => {
  emit('navigate', view)
  if (isMobile.value) {
    emit('update:collapsed', true)
  }
}

// 处理遮罩点击
const handleMaskClick = () => {
  emit('update:collapsed', true)
}

// 监听窗口大小变化
onMounted(() => {
  checkScreenSize()
  window.addEventListener('resize', checkScreenSize)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkScreenSize)
})
</script>

<style scoped>
/* 确保按钮始终在最上层 */
button {
  z-index: 50;
}

/* 优化移动端体验 */
@media (max-width: 768px) {
  aside {
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  }
}
</style>