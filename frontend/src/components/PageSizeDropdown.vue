<template>
  <div class="relative w-32" ref="dropdownRef">
    <div
      class="border border-gray-300 dark:border-gray-600 rounded-lg p-2 min-h-[40px] cursor-pointer bg-white dark:bg-gray-700 flex items-center justify-between hover:border-blue-400 transition-colors"
      @click="toggleDropdown"
    >
      <span class="text-gray-800 dark:text-gray-100 font-medium">{{ selectedLabel }}</span>
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

    <div
      v-if="dropdownOpen"
      class="absolute z-10 mt-1 w-full bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg shadow-md max-h-48 overflow-y-auto"
    >
      <div
        v-for="size in options"
        :key="size"
        @click="selectOption(size)"
        class="px-3 py-2 cursor-pointer flex justify-between items-center hover:bg-blue-100 dark:hover:bg-blue-600 transition-colors"
      >
        <span
          :class="size === modelValue
                    ? 'text-blue-600 dark:text-blue-400 font-semibold'
                    : 'text-gray-800 dark:text-gray-100'"
        >
          {{ size }} 条/页
        </span>
        <span v-if="size === modelValue" class="text-blue-600 dark:text-blue-400 font-semibold">✔</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  modelValue: { type: Number, default: 10 },
  options: { type: Array, default: () => [5, 10, 20, 50, 100] }
})
const emit = defineEmits(['update:modelValue'])

const dropdownOpen = ref(false)
const dropdownRef = ref(null)
const selectedLabel = computed(() => `${props.modelValue} 条/页`)

function toggleDropdown() {
  dropdownOpen.value = !dropdownOpen.value
}

function selectOption(size) {
  emit('update:modelValue', size)
  dropdownOpen.value = false
}

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
