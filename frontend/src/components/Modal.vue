<template>
  <!-- 遮罩层 -->
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <!-- 弹窗主体 -->
    <div
      class="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-xl mx-4 p-6 relative animate-fadeIn transition-colors"
    >
      <!-- 关闭按钮 -->
      <span
        @click="$emit('close')"
        class="absolute top-2 right-4 text-gray-500 dark:text-gray-300 hover:text-gray-700 dark:hover:text-white text-xl font-bold cursor-pointer select-none transition-colors"
      >
        &times;
      </span>

      <!-- 标题 -->
      <h2
        v-if="title"
        class="text-xl font-semibold mb-4 text-center text-gray-700 dark:text-gray-200 transition-colors"
      >
        {{ title }}
      </h2>

      <!-- 主体内容 -->
      <div class="overflow-y-auto max-h-[70vh] space-y-4">
        <slot />
      </div>

      <!-- 底部操作区 -->
      <div
        v-if="$slots.footer"
        class="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700 flex justify-end space-x-3 transition-colors"
      >
        <slot name="footer" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

defineProps({
  title: { type: String, default: '' }
})
defineEmits(['close'])

// ⚡ 自动给插槽里的常用控件加暗/亮模式类
onMounted(() => {
  const container = document.querySelector('.animate-fadeIn')
  if (!container) return

  const controls = container.querySelectorAll('input, select, textarea, button')
  controls.forEach(el => {
    // 输入框/选择框/文本域
    if (['INPUT', 'SELECT', 'TEXTAREA'].includes(el.tagName)) {
      el.classList.add(
        'bg-white', 'dark:bg-gray-700',
        'text-gray-700', 'dark:text-white',
        'border', 'border-gray-300', 'dark:border-gray-600',
        'rounded', 'px-3', 'py-2', 'focus:outline-none', 'focus:ring-2', 'focus:ring-blue-500', 'transition-colors'
      )
    }
    // 按钮
    if (el.tagName === 'BUTTON') {
      el.classList.add(
        'bg-blue-600', 'dark:bg-blue-500',
        'text-white', 'dark:text-white',
        'px-4', 'py-2', 'rounded', 'hover:bg-blue-700', 'dark:hover:bg-blue-600', 'transition-colors'
      )
    }
  })
})
</script>

<style scoped>
/* 弹窗淡入动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fadeIn {
  animation: fadeIn 0.2s ease-out;
}

/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-thumb {
  background-color: #ccc;
  border-radius: 3px;
}
::-webkit-scrollbar-track {
  background-color: transparent;
}
/* 暗模式滚动条 */
.dark ::-webkit-scrollbar-thumb {
  background-color: #4b5563; /* gray-600 */
}
</style>
