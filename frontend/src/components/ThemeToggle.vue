<template>
  <button
    @click="toggleTheme"
    class="px-2 py-1 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-200 text-sm"
  >
    {{ isDark ? '🌙 暗' : '☀️ 亮' }}
  </button>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isDark = ref(false)

const toggleTheme = () => {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

onMounted(() => {
  // 优先读取本地存储
  const saved = localStorage.getItem('theme')
  if (saved === 'dark') {
    isDark.value = true
    document.documentElement.classList.add('dark')
  } else if (saved === 'light') {
    isDark.value = false
    document.documentElement.classList.remove('dark')
  } else {
    // 默认跟随系统偏好
    isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    document.documentElement.classList.toggle('dark', isDark.value)
  }

  // 监听系统主题变化
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    if (!localStorage.getItem('theme')) {
      isDark.value = e.matches
      document.documentElement.classList.toggle('dark', isDark.value)
    }
  })
})
</script>
