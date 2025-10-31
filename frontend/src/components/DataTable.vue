<template>
  <div :class="['shadow rounded-lg p-4 transition-colors',
                theme.darkMode ? 'bg-gray-800 text-white' : 'bg-white text-gray-700']">
    <!-- 标题 -->
    <h2 class="text-lg font-semibold mb-2" :class="theme.darkMode ? 'text-white' : 'text-gray-700'">
      {{ title }}
    </h2>

    <!-- 顶部搜索 + 操作按钮 -->
    <div class="flex flex-col md:flex-row md:justify-between md:items-center mb-4 space-y-2 md:space-y-0">
      <input
        v-model="searchQuery"
        type="text"
        :placeholder="`搜索${title}...`"
        :class="['border rounded px-3 py-2 w-full md:w-64 focus:outline-none focus:ring-2 focus:ring-blue-500',
                 theme.darkMode ? 'border-gray-600 bg-gray-700 text-white' : 'border-gray-300 bg-white text-gray-700']"
      />
      <div class="flex space-x-2">
        <slot name="actions"></slot>
      </div>
    </div>

    <!-- 表格 -->
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y transition-colors"
             :class="theme.darkMode ? 'divide-gray-700' : 'divide-gray-200'">
        <thead :class="theme.darkMode ? 'bg-gray-700' : 'bg-gray-50'">
          <tr>
            <th v-for="col in columns" :key="col.key"
                class="px-4 py-2 text-left text-sm font-medium"
                :class="theme.darkMode ? 'text-gray-200' : 'text-gray-700'">
              {{ col.label }}
            </th>
            <th class="px-4 py-2 text-left text-sm font-medium"
                :class="theme.darkMode ? 'text-gray-200' : 'text-gray-700'">
              操作
            </th>
          </tr>
        </thead>
        <tbody :class="theme.darkMode ? 'divide-gray-700' : 'divide-gray-200'">
          <tr v-for="row in pagedData" :key="row.id"
              :class="['hover:bg-gray-50 dark:hover:bg-gray-700']">
            <td v-for="col in columns" :key="col.key" class="px-4 py-2 text-sm"
                :class="theme.darkMode ? 'text-white' : 'text-gray-700'">
              {{ row[col.key] }}
            </td>
            <td class="px-4 py-2 text-sm" :class="theme.darkMode ? 'text-white' : 'text-gray-700'">
              <slot name="row-actions" :row="row"></slot>
            </td>
          </tr>
          <tr v-if="pagedData.length === 0">
            <td :colspan="columns.length + 1" class="px-4 py-2 text-center text-gray-400 dark:text-gray-400">
              暂无数据
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div class="flex justify-end items-center mt-4 space-x-2">
      <button @click="prevPage" :disabled="page===1"
              class="px-3 py-1 rounded transition"
              :class="theme.darkMode ? 'bg-gray-700 disabled:opacity-50' : 'bg-gray-200 disabled:opacity-50'">
        上一页
      </button>
      <span>{{ page }} / {{ totalPages }}</span>
      <button @click="nextPage" :disabled="page===totalPages"
              class="px-3 py-1 rounded transition"
              :class="theme.darkMode ? 'bg-gray-700 disabled:opacity-50' : 'bg-gray-200 disabled:opacity-50'">
        下一页
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useThemeStore } from '../store/themeStore.js'

const props = defineProps({
  title: { type: String, default: '数据表' },  // 新增 title
  columns: { type: Array, required: true },
  data: { type: Array, required: true },
  pageSize: { type: Number, default: 10 }
})

const theme = useThemeStore()
const searchQuery = ref('')
const page = ref(1)

const filteredData = computed(() => {
  if (!searchQuery.value) return props.data
  return props.data.filter(row =>
    Object.values(row).some(val => String(val).toLowerCase().includes(searchQuery.value.toLowerCase()))
  )
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredData.value.length / props.pageSize)))

const pagedData = computed(() => {
  const start = (page.value - 1) * props.pageSize
  return filteredData.value.slice(start, start + props.pageSize)
})

function nextPage() { if(page.value<totalPages.value) page.value++ }
function prevPage() { if(page.value>1) page.value-- }

watch(filteredData, () => { page.value = 1 })
</script>
