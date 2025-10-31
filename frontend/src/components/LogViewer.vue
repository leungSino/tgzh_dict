<template>
  <DataTable
    title="操作日志"
    :columns="columns"
    :data="logs"
  >
    <template #actions>
      <button class="px-3 py-1 bg-gray-500 text-white rounded hover:bg-gray-600"
              @click="clearLogs">清空日志</button>
    </template>

    <template #row-actions="{ row }">
      <button class="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600"
              @click="deleteLog(row.id)">删除</button>
    </template>
  </DataTable>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DataTable from './DataTable.vue'
import api from '../api/api.js'

const columns = [
  { key: 'user', label: '操作用户' },
  { key: 'action', label: '操作内容' },
  { key: 'time', label: '时间' }
]

const logs = ref([])

async function loadLogs() {
  const res = await api.searchLogs('')
  logs.value = res.data || []
}

async function deleteLog(id) {
  await api.deleteLog(id)
  loadLogs()
}

async function clearLogs() {
  if(confirm('确认清空所有日志吗？')) {
    await api.clearLogs()
    loadLogs()
  }
}

onMounted(loadLogs)
</script>
