<template>
  <div class="shadow rounded-lg p-4 bg-white dark:bg-gray-800 text-gray-700 dark:text-white transition-colors">
    <div class="flex justify-between items-center mb-4">
      <slot name="actions"></slot>
      <input
        v-model="searchQuery"
        type="text"
        placeholder="搜索..."
        class="border rounded px-3 py-2 w-64 focus:outline-none focus:ring-2 focus:ring-blue-500
               bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-700
               dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
      />
    </div>

    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th v-for="col in columns" :key="col.key" class="px-4 py-2 text-left text-sm font-medium text-gray-700 dark:text-gray-200">
              {{ col.label }}
            </th>
            <th class="px-4 py-2 text-left text-sm font-medium text-gray-700 dark:text-gray-200">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-for="row in data" :key="row.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
            <td v-for="col in columns" :key="col.key" class="px-4 py-2 text-sm text-gray-700 dark:text-gray-200">
              {{ getField(row, col.key) }}
            </td>
            <td class="px-4 py-2 text-sm text-gray-700 dark:text-gray-200">
              <slot name="row-actions" :row="row"></slot>
            </td>
          </tr>
          <tr v-if="!loading && data.length === 0">
            <td :colspan="columns.length + 1" class="px-4 py-2 text-center text-gray-400 dark:text-gray-400">暂无数据</td>
          </tr>
          <tr v-if="loading">
            <td :colspan="columns.length + 1" class="px-4 py-4 text-center text-gray-400 dark:text-gray-400">加载中...</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div class="flex flex-wrap justify-between items-center mt-4 space-y-2 sm:space-y-0">
      <div class="flex items-center space-x-2">
        <button
          @click="prevPage"
          :disabled="page === 1 || loading"
          class="px-3 py-1 rounded transition bg-gray-200 dark:bg-gray-700 disabled:opacity-50"
        >
          上一页
        </button>
        <span>第 {{ page }} / {{ totalPages }} 页，共 {{ total }} 条</span>
        <button
          @click="nextPage"
          :disabled="page === totalPages || loading"
          class="px-3 py-1 rounded transition bg-gray-200 dark:bg-gray-700 disabled:opacity-50"
        >
          下一页
        </button>
      </div>

      <PageSizeDropdown v-model="pageSize" @update:modelValue="changePageSize" />
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import PageSizeDropdown from './PageSizeDropdown.vue'

const props = defineProps({
  columns: { type: Array, required: true },
  fetchData: { type: Function, required: true },
  pageSize: { type: Number, default: 10 }
})

const searchQuery = ref('')
const page = ref(1)
const pageSize = ref(props.pageSize)
const total = ref(0)
const data = ref([])
const loading = ref(false)

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize.value)))

async function loadData() {
  loading.value = true
  try {
    const res = await props.fetchData(searchQuery.value.trim(), page.value, pageSize.value)
    data.value = res.items || []
    total.value = res.total || 0
  } catch (err) {
    console.error('加载数据出错:', err)
    data.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

let searchTimer
watch(searchQuery, () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    page.value = 1
    loadData()
  }, 400)
})

function nextPage() {
  if (page.value < totalPages.value) {
    page.value++
    loadData()
  }
}

function prevPage() {
  if (page.value > 1) {
    page.value--
    loadData()
  }
}

function changePageSize(size) {
  page.value = 1
  pageSize.value = size
  loadData()
}

function getField(row, key) {
  return key.split('.').reduce((obj, k) => obj?.[k], row) ?? '-'
}

function reload() {
  loadData()
}
defineExpose({ reload })

onMounted(loadData)
</script>
