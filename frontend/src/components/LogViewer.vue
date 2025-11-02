<template>
  <DataTable title="操作日志" :columns="columns" :data="logs">
    <template #actions>
      <button @click="clearLogs" class="px-3 py-1 bg-gray-600 text-white rounded hover:bg-gray-700">清空日志</button>
    </template>

    <template #row-actions="{ row }">
      <button @click="deleteLog(row._id)" class="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600">删除</button>
    </template>
  </DataTable>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DataTable from './DataTable.vue'
import api from '@/api/api.js'

const columns = [
  { key: 'user', label: '操作用户' },
  { key: 'action', label: '操作内容' },
  { key: 'time', label: '时间' }
]

const logs = ref([])

async function loadLogs() {
  try {
    const res = await api.getLogs?.()
    logs.value = (res && res.data) ? res.data : (res || [])
  } catch (e) {
    logs.value = []
  }
}

async function deleteLog(id) {
  if (!confirm('确认删除该日志？')) return
  await api.deleteLog?.(id)
  await loadLogs()
}

async function clearLogs() {
  if (!confirm('确认清空所有日志？')) return
  await api.clearLogs?.()
  await loadLogs()
}

onMounted(loadLogs)
</script>
