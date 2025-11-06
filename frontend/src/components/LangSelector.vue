<template>
  <div class="relative w-full" ref="dropdownRef">
    <!-- 自定义选择框 -->
    <div
      class="border border-gray-300 dark:border-gray-600 rounded-lg p-2 min-h-[40px] cursor-pointer bg-white dark:bg-gray-700 flex items-center justify-between hover:border-blue-400 transition-colors"
      @click="toggleDropdown"
    >
      <span v-if="selectedLabel" class="text-gray-800 dark:text-gray-100 font-medium">{{ selectedLabel }}</span>
      <span v-else class="text-gray-400 dark:text-gray-400">{{ placeholder }}</span>
      <svg
        class="w-4 h-4 text-gray-500 dark:text-gray-300 ml-2 transform transition-transform"
        :class="{ 'rotate-180': dropdownOpen }"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
      </svg>
    </div>

    <!-- 下拉选项 -->
    <div
      v-if="dropdownOpen"
      class="absolute z-10 mt-1 w-full bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg shadow-md max-h-48 overflow-y-auto"
    >
      <div
        v-for="(label, code) in options"
        :key="code"
        @click="selectOption(code)"
        class="px-3 py-2 cursor-pointer flex justify-between items-center hover:bg-blue-100 dark:hover:bg-blue-600 transition-colors"
      >
        <span
          :class="code === modelValue
                    ? 'text-blue-600 dark:text-blue-400 font-semibold'
                    : 'text-gray-800 dark:text-gray-100'"
        >
          {{ label }}
        </span>
        <span v-if="code === modelValue" class="text-blue-600 dark:text-blue-400 font-semibold">✔</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  modelValue: String,
  placeholder: { type: String, default: '请选择语言' }
})
const emit = defineEmits(['update:modelValue'])

const options = {
  zh: '中文',
  tg: '塔吉克语',
  ru: '俄语',
  en: '英语'
}

const dropdownOpen = ref(false)
const dropdownRef = ref(null)

const selectedLabel = computed(() => options[props.modelValue] || '')

function toggleDropdown() {
  dropdownOpen.value = !dropdownOpen.value
}

function selectOption(code) {
  emit('update:modelValue', code)
  dropdownOpen.value = false
}

// 点击外部关闭
function handleClickOutside(e) {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target)) {
    dropdownOpen.value = false
  }
}
onMounted(() => document.addEventListener('click', handleClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', handleClickOutside))
</script>

<style scoped>
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-thumb {
  background-color: #ccc;
  border-radius: 3px;
}
</style>
