import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const darkMode = ref(localStorage.getItem('theme') === 'dark' || window.matchMedia('(prefers-color-scheme: dark)').matches)

  const toggleTheme = () => {
    darkMode.value = !darkMode.value
    document.documentElement.classList.toggle('dark', darkMode.value)
    localStorage.setItem('theme', darkMode.value ? 'dark' : 'light')
  }

  // 初始同步
  watch(darkMode, val => {
    document.documentElement.classList.toggle('dark', val)
  }, { immediate: true })

  return { darkMode, toggleTheme }
})
