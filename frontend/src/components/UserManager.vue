<template>
  <DataTable title="用户管理" :columns="columns" :data="users">
    <template #actions>
      <button @click="openAdd" class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700">新增用户</button>
    </template>

    <template #row-actions="{ row }">
      <button @click="deleteUser(row._id)" class="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600">删除</button>
    </template>
  </DataTable>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DataTable from './DataTable.vue'
import api from '@/api/api.js'

const columns = [
  { key: 'username', label: '用户名' },
  { key: 'role', label: '角色' },
  { key: 'created_at', label: '创建时间' }
]

const users = ref([])

async function loadUsers() {
  try {
    const res = await api.searchUsers?.('') || { data: [] }
    users.value = res.data || []
  } catch (e) {
    users.value = []
  }
}

async function openAdd() {
  alert('新增用户弹窗 / 表单逻辑（管理员可在这里添加用户）')
}

async function deleteUser(id) {
  if (!confirm('确认删除该用户？')) return
  await api.deleteUser?.(id)
  await loadUsers()
}

onMounted(loadUsers)
</script>
