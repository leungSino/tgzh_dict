<template>
  <div class="shadow rounded-lg p-4 bg-white dark:bg-gray-800 text-gray-700 dark:text-white transition-colors">
    <div class="flex justify-between items-center mb-4">
      <slot name="actions"></slot>
      <input
        v-model="searchQuery"
        type="text"
        placeholder="搜索..."
        class="border rounded px-3 py-2 w-64 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
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
          <tr v-for="row in pagedData" :key="row.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
            <td v-for="col in columns" :key="col.key" class="px-4 py-2 text-sm text-gray-700 dark:text-gray-200">
              {{ getField(row, col.key) }}
            </td>
            <td class="px-4 py-2 text-sm text-gray-700 dark:text-gray-200">
              <slot name="row-actions" :row="row"></slot>
            </td>
          </tr>
          <tr v-if="pagedData.length === 0">
            <td :colspan="columns.length + 1" class="px-4 py-2 text-center text-gray-400 dark:text-gray-400">暂无数据</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="flex justify-end items-center mt-4 space-x-2">
      <button @click="prevPage" :disabled="page===1" class="px-3 py-1 rounded transition bg-gray-200 dark:bg-gray-700 disabled:opacity-50">上一页</button>
      <span>{{ page }} / {{ totalPages }}</span>
      <button @click="nextPage" :disabled="page===totalPages" class="px-3 py-1 rounded transition bg-gray-200 dark:bg-gray-700 disabled:opacity-50">下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  columns: { type: Array, required: true },
  data: { type: Array, required: true },
  pageSize: { type: Number, default: 10 }
})

const searchQuery = ref('')
const page = ref(1)

const filteredData = computed(() => {
  if (!searchQuery.value) return props.data
  const q = searchQuery.value.toLowerCase()
  return props.data.filter(row =>
    Object.values(row).some(val => String(val).toLowerCase().includes(q))
  )
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredData.value.length / props.pageSize)))

const pagedData = computed(() => {
  const start = (page.value - 1) * props.pageSize
  return filteredData.value.slice(start, start + props.pageSize)
})

function nextPage() { if (page.value < totalPages.value) page.value++ }
function prevPage() { if (page.value > 1) page.value-- }

watch(filteredData, () => page.value = 1)

function getField(row, key) {
  return key.split('.').reduce((obj, k) => obj?.[k], row) || '-'
}
</script>
