<template>
  <div class="relative w-full" ref="dropdownRef">
    <!-- 自定义选择框 -->
    <div
      class="border border-gray-300 dark:border-gray-600 rounded-lg p-2 min-h-[40px] cursor-pointer bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 flex flex-wrap items-center gap-1 hover:border-blue-400 transition-colors"
      @click="toggleDropdown"
    >
      <!-- 已选内容 -->
      <template v-if="selectedValues.length">
        <span
          v-for="code in selectedValues"
          :key="code"
          class="bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 px-2 py-1 rounded-full text-sm flex items-center"
        >
          {{ posOptions[code] }}
          <button
            type="button"
            @click.stop="removeSelection(code)"
            class="ml-1 text-blue-500 dark:text-blue-200 hover:text-blue-700 dark:hover:text-blue-400 font-bold"
          >
            ×
          </button>
        </span>
      </template>
      <span v-else class="text-gray-400 dark:text-gray-400">{{ placeholder }}</span>

      <!-- 下拉箭头 -->
      <svg
        class="w-4 h-4 text-gray-500 dark:text-gray-300 ml-auto transition-transform"
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
        v-for="(cn, code) in posOptions"
        :key="code"
        @click="toggleSelection(code)"
        class="px-3 py-2 cursor-pointer hover:bg-blue-100 dark:hover:bg-blue-600 flex items-center justify-between transition-colors"
      >
        <span
          :class="selectedValues.includes(code)
            ? 'text-blue-600 dark:text-blue-400 font-semibold'
            : 'text-gray-800 dark:text-gray-100'"
        >
          {{ cn }}
        </span>
        <input type="checkbox" :checked="selectedValues.includes(code)" @change.stop />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  placeholder: { type: String, default: '请选择词性（可多选）' }
})

const emit = defineEmits(['update:modelValue'])

const posOptions = {
  noun: '名词',
  verb: '动词',
  adj: '形容词',
  adv: '副词',
  pron: '代词',
  prep: '介词',
  conj: '连词',
  part: '助词',
  num: '数词',
  interj: '叹词',
  onomat: '拟声词'
}

const selectedValues = ref([...props.modelValue])
const dropdownOpen = ref(false)
const dropdownRef = ref(null)

watch(() => props.modelValue, val => {
  selectedValues.value = [...(val || [])]
})

function toggleDropdown() {
  dropdownOpen.value = !dropdownOpen.value
}

function toggleSelection(code) {
  const idx = selectedValues.value.indexOf(code)
  if (idx >= 0) selectedValues.value.splice(idx, 1)
  else selectedValues.value.push(code)
  emit('update:modelValue', [...selectedValues.value])
}

function removeSelection(code) {
  selectedValues.value = selectedValues.value.filter(c => c !== code)
  emit('update:modelValue', [...selectedValues.value])
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
